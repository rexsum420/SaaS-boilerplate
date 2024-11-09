from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from saas.context_processor import get_role
from employees.models import Employee
from employees.serializers import EmployeeSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee
from .forms import EmployeeForm
from django.db import transaction
from django.contrib import messages

def create_employee(request):
    employee_form = EmployeeForm(request.POST or None)
    user_form = UserCreationForm(request.POST or None)

    if request.method == 'POST':
        # Check if EmployeeForm and UserCreationForm are valid
        if employee_form.is_valid():
            with transaction.atomic():
                # Get the selected user from the form
                user = employee_form.cleaned_data.get('user')
                
                # If no user is selected, create a new one using UserCreationForm
                if not user and user_form.is_valid():
                    user = user_form.save()

                # Associate the created or selected user with the Employee and save
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
                
                messages.success(request, 'Employee created successfully.')
                return redirect('employee_list')  # Adjust to your actual employee list view or relevant redirect
        else:
            messages.error(request, "Please correct the errors below.")

    context = {
        'employee_form': employee_form,
        'user_form': user_form,
    }
    return render(request, 'accounts/create-employee.html', context)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            role = get_role(self.request.user)
            if role in ['Owner', 'Admin', 'Manager', 'Employee']:             
                employees = Employee.objects.all()
                qs = employees
                return qs
        return None
    
    def perform_create(self, serializer):
        if self.request.user.role in ['Owner', 'Admin', 'Manager']:
            raise PermissionDenied("Employees can not create new employee accounts.")
        serializer.save()