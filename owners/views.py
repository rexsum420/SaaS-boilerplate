from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from saas.context_processor import get_role
from owners.models import Owner
from management.models import Manager
from employees.models import Employee
from owners.serializers import OwnerSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            role = get_role(self.request.user)
            if role == 'Owner' or role == 'Admin':            
                owners = Owner.objects.all()
                qs = owners
                return qs
        return None
    
    def perform_create(self, serializer):
        if self.request.user.role in ['Owner', 'Admin']:
            raise PermissionDenied("Only owners and admins can create owner accounts.")