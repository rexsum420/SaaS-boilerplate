from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from menu_app.context_processor import get_role
from owners.models import Owner
from management.models import Manager
from employees.models import Employee
from management.serializers import ManagerSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            role = get_role(self.request.user)
            if role == 'Owner' or role == 'Admin' or role == 'Manager':             
                managers = Manager.objects.all()
                qs = managers
                return qs
        return None
    
    def perform_create(self, serializer):
        # Restrict account creation to specific roles if needed
        if self.request.user.role in ['Owner', 'Admin']:
            raise PermissionDenied("Only owners and admins can create manager accounts.")
        serializer.save()