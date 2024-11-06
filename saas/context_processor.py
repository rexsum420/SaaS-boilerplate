from owners.models import Owner
from management.models import Manager
from employees.models import Employee

def get_role(obj):
    if Owner.objects.filter(user=obj).exists():
        return 'Owner'
    elif Manager.objects.filter(user=obj).exists():
        return 'Manager'
    elif Employee.objects.filter(user=obj).exists():
        return 'Employee'
    if obj.is_admin:
        return 'Admin'
    return 'Unknown'

def role_processor(request):
    if request.user.is_authenticated:
        if user != request.user:
            user = request.user
            role = get_role(request.user)
    else:
        user = None
        role = None   
    return {
        'role': role
    }