from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from owners.models import Owner
from management.models import Manager, ManagerEntry
from employees.models import Employee, TimeEntry
from django.shortcuts import render, redirect, get_object_or_404
from admin_volt.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
from django.db.models import Sum, F, DateTimeField
from django.db.models.functions import TruncHour
from orders.models import Order
from django.views.decorators.http import require_POST


from django.contrib.auth.decorators import login_required
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

@login_required(login_url="login")
def admin_site(request):
    return render(request, 'admin.html')

# Authentication
def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      print("Account created successfully!")
      form.save()
      return redirect('/accounts/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = { 'form': form }
  return render(request, 'accounts/sign-up.html', context)

class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'accounts/sign-in.html'

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/reset-password.html'
  form_class = UserSetPasswordForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')
@login_required(login_url="login")
def index(request):
  return render(request, 'pages/index.html')
@login_required(login_url="login")
def enter_pin_view(request):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        # Assume `ssn` field only stores last 4 digits
        employee = Employee.objects.filter(pin=pin).first()
        if employee:
            request.session['employee_id'] = employee.id  # Store employee id in session
            return redirect('clock_in_out')
        else:
            return render(request, 'admin/index.html', {'error': 'Invalid PIN. Please try again.'})
    return render(request, 'admin/index.html')

@login_required(login_url="login")
def clock_in_out_view(request):
    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect('enter_pin')

    employee = get_object_or_404(Employee, id=employee_id)
    
    chicago_tz = pytz.timezone("America/Chicago")
    chicago_time = datetime.now(chicago_tz).date()
    today = chicago_time
    time_entry = TimeEntry.objects.filter(employee=employee, day=today).order_by('-clock_in').first()


    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'clock_in':
                employee.clock_in()
                message = "Clocked in successfully."
            elif action == 'clock_out':
                employee.clock_out()
                message = "Clocked out successfully."
            return redirect('admin:index')
        except ValueError as e:
            return render(request, 'clock_in_out.html', {
                'employee': employee,
                'error': str(e),
                'time_entry': time_entry
            })
            
    return render(request, 'clock_in_out.html', {
        'employee': employee,
        'time_entry': time_entry
    })

@login_required(login_url="login")
def dashboard(request):
    # Set timezone and get the current date in Chicago time
    chicago_tz = pytz.timezone("America/Chicago")
    chicago_time = datetime.now(chicago_tz)
    today = chicago_time.date()

    # Generate a list of all hours in the day (0 through 23)
    all_hours = [chicago_time.replace(hour=h, minute=0, second=0, microsecond=0) for h in range(24)]

    # Fetch the sales data, grouped by hour
    hourly_sales = (
        Order.objects.filter(created_at__date=today)
        .annotate(hour=TruncHour('created_at', output_field=DateTimeField()))
        .values('hour')
        .annotate(total_sales=Sum(F('line_items__quantity') * F('line_items__price')))
        .order_by('hour')
    )

    # Create a dictionary of sales by hour for easy lookup
    sales_dict = {sale['hour'].hour: sale['total_sales'] for sale in hourly_sales}

    # For each hour, if no sale exists, default to 0, and format the hour as an integer
    hourly_sales_with_defaults = [
        {
            'hour': hour.hour,
            'total_sales': sales_dict.get(hour.hour, 0)
        }
        for hour in all_hours
    ]

    current_employees = TimeEntry.objects.filter(day=today, clock_out=None)
    finished_shifts = TimeEntry.objects.filter(day=today).exclude(clock_out=None)
    current_managers = ManagerEntry.objects.filter(day=today, clock_out=None)
    finished_managers = ManagerEntry.objects.filter(day=today).exclude(clock_out=None)

    return render(request, 'pages/dashboard/dashboard.html', {
        'current_employees': current_employees,
        'finished_shifts': finished_shifts,
        'current_managers': current_managers,
        'finished_managers': finished_managers,
        'today': chicago_time,
        'hourly_sales': hourly_sales_with_defaults,
    })

@login_required(login_url="login")
def weekly_hours(request, user_id):
    # Check if the user is an employee or manager
    employee = Employee.objects.filter(user__id=user_id).first()
    manager = Manager.objects.filter(user__id=user_id).first()

    # Get start of the week from session or use default (0 = Monday)
    start_of_week = request.session.get('start_of_week', 0)  # Default to Monday (0)
    
    # Get today's date
    today = timezone.now().date()

    # Calculate the start of the week based on user's start of week preference (0-6)
    start_of_week_date = today - timedelta(days=(today.weekday() - start_of_week) % 7)

    # Fetch weekly hours for either employee or manager
    if employee:
        weekly_entries = TimeEntry.objects.filter(employee=employee, clock_in__date__gte=start_of_week_date)
        user = employee.user
    elif manager:
        weekly_entries = ManagerEntry.objects.filter(manager=manager, clock_in__date__gte=start_of_week_date)
        user = manager.user
    else:
        weekly_entries = None
        user = None

    # Calculate total weekly hours
    total_hours = sum(entry.duration for entry in weekly_entries) if weekly_entries else 0

    return render(request, 'hours/weekly_hours.html', {
        'user': user,
        'weekly_entries': weekly_entries,
        'total_hours': total_hours,
        'start_of_week': start_of_week_date,
    })

@login_required(login_url="login")
def report_labor(request):
    # Get user settings from session or use defaults
    start_of_week = request.session.get('start_of_week', 0)  # Default to Monday (0)
    pay_period_duration = request.session.get('pay_period_duration', 7)  # Default to weekly (7 days)

    # Initialize arrays for storing totals and labels
    pay_period_totals = []
    period_labels = []

    # Get the current date and the start of the year
    current_date = timezone.now().date()
    start_of_year = current_date.replace(month=1, day=1)

    # Align start of the first pay period to user-defined start of week
    start_of_period = start_of_year - timedelta(days=(start_of_year.weekday() - start_of_week) % 7)

    # Loop through each pay period until the current date
    while start_of_period <= current_date:
        end_of_period = start_of_period + timedelta(days=pay_period_duration - 1)

        # Calculate total wages for employees within the pay period
        employee_entries = TimeEntry.objects.filter(
            employee__in=Employee.objects.all(),
            clock_in__date__range=(start_of_period, end_of_period)
        )
        total_employee_wages = sum(float(entry.duration) * float(entry.employee.pay_rate) for entry in employee_entries)

        # Calculate total wages for managers within the pay period
        manager_entries = ManagerEntry.objects.filter(
            manager__in=Manager.objects.all(),
            clock_in__date__range=(start_of_period, end_of_period)
        )
        total_manager_wages = sum(float(entry.duration) * float(entry.manager.pay_rate) for entry in manager_entries)

        # Append total wages for the pay period
        pay_period_totals.append(total_employee_wages + total_manager_wages)

        # Add a label for the first period of each month or when the period crosses into a new month
        if start_of_period.day <= 7 or start_of_period.month != end_of_period.month:
            period_labels.append(f"{start_of_period.strftime('%b %d')} - {end_of_period.strftime('%b %d')}")
        else:
            period_labels.append('')  # Empty label for other periods

        # Move to the next pay period
        start_of_period += timedelta(days=pay_period_duration)

    # Render the template with calculated totals and labels
    return render(request, 'pages/report_labor.html', {
        'weekly_totals': pay_period_totals,
        'week_labels': period_labels,
    })


def set_user_preferences(request):
    if request.method == 'POST':        
        # Get the start of week and pay period duration from POST data
        start_of_week = int(request.POST.get('start_of_week', 0))
        pay_period_duration = int(request.POST.get('pay_period_duration', 7))

        # Save these values in the session
        request.session['start_of_week'] = start_of_week
        request.session['pay_period_duration'] = pay_period_duration

        return redirect('dashboard')

    return render(request, 'pages/settings.html')