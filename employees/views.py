from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from saas.context_processor import get_role
from employees.models import Employee
from employees.serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            role = get_role(self.request.user)
            if role == 'Owner' or role == 'Admin' or role == 'Manager' or role == 'Employee':             
                employees = Employee.objects.all()
                qs = employees
                return qs
        return None
    
    def perform_create(self, serializer):
        if self.request.user.role in ['Owner', 'Admin', 'Manager']:
            raise PermissionDenied("Employees can not create new employee accounts.")
        serializer.save()