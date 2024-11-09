from owners.models import Owner
from management.models import Manager
from employees.models import Employee
from django.urls import reverse, NoReverseMatch
from datetime import timedelta
from django.utils import timezone

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

def settings_processor(request):
    # Default start of the week is Monday (0)
    user_start_of_week = request.session.get('start_of_week', 0)

    # Default pay period duration is weekly (7 days)
    pay_period_duration = request.session.get('pay_period_duration', 7)

    # Get today's date
    today = timezone.now().date()

    # Calculate the start of the current week based on user's start of week preference (0-6)
    # Calculate the number (0-6) of the day of the week from user's start_of_week preference
    start_of_week_number = (today.weekday() - user_start_of_week) % 7

    # Optionally, calculate the start of the pay period based on the chosen duration
    start_of_pay_period = today - timedelta(days=(today.toordinal() % pay_period_duration))

    return {
        'start_of_week': start_of_week_number,
        'pay_period_duration': pay_period_duration,
        'start_of_pay_period': start_of_pay_period,
    }