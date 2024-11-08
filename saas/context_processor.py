from owners.models import Owner
from management.models import Manager
from employees.models import Employee
from django.urls import reverse, NoReverseMatch

def get_safe_url(view_name, *args, **kwargs):
    """
    Attempt to reverse a URL for the given view name with optional args and kwargs.
    If the URL cannot be resolved, it will return None.
    """
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        print(f"Warning: Could not reverse URL for view '{view_name}' with args={args} and kwargs={kwargs}.")
        return None  # Or use a default URL like '/'

def url_utils(request):
    """
    Context processor to add `get_safe_url` to the template context.
    """
    return {
        'get_safe_url': get_safe_url
    }
    
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
    role=None
    if request.user.is_authenticated:
        user = request.user
        if user != request.user:
            user = request.user
            role = get_role(request.user)
    else:
        user = None
        role = None   
    return {
        'role': role
    }