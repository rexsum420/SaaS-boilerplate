from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from owners.models import Owner
from management.models import Manager
from employees.models import Employee

def activate(request, username, token):
    try:
        tokn = Token.objects.get(key=token)
        user = tokn.user
        if user.username.lower() == username.lower():
            user = tokn.user
        else:
            user = None
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    try:
        if user is not None:
            owners = Owner.objects.filter(user=user)
            managers = Manager.objects.filter(user=user)
            employees = Employee.objects.filter(user=user)        
            if len(owners) == 1:
                owners.email_confirmed = True
                owners.save()
            elif len(owners) > 1:
                return PermissionDenied('Too many owner objects associated to that user returned')
            if len(managers) == 1:
                managers.email_confirmed = True
                managers.save()
            elif len(managers) > 1:
                return PermissionDenied('Too many manager objects associated to that user returned')
            if len(employees) == 1:
                employees.email_confirmed = True
                employees.save()
            elif len(employees) > 1:
                return PermissionDenied('Too many employee objects associated to that user returned')
            return render(request, 'email_verified.html', {'user': user})
        else:
            return HttpResponse('email not verified')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Token.DoesNotExist):
        return HttpResponse('Invalid verification link.')   
User = get_user_model()

class CheckTokenView(APIView):
    def get(self, request, token, format=None):
        try:
            tokn = Token.objects.get(key=token)
            return Response({'detail': 'Token verified', 'user': tokn.user.username}, status=HTTP_200_OK)
        except Token.DoesNotExist:
            raise PermissionDenied('Token doesn\'t match any user tokens')

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user and user.is_authenticated:
            if user.is_staff:
                return User.objects.all()
            else:
                return User.objects.filter(id=user.id)
        return User.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return super().get_permissions()

    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        return super().get_authenticators()

    def perform_create(self, serializer):
        return PermissionDenied('Please create a user from the Role API (eg. Owner, Manager, Employee)')

    def perform_destroy(self, instance):
        return PermissionDenied('Users can not be deleted')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not self.request.user == instance:
            raise PermissionDenied("You do not have permission to view this product.")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)