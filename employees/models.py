from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from saas.fields import SSNField
from rest_framework.authtoken.models import Token
from datetime import timedelta


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=24, blank=True, null=True)
    last_name = models.CharField(max_length=24, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    last_active = models.CharField(max_length=512, blank=True, null=True)
    ssn = SSNField(unique=True, blank=True, null=True)
    pay_rate = models.DecimalField(max_digits=5, decimal_places=2, default=7.50)
    
    def __str__(self):
        return self.user.username

    def clock_in(self):
        # Create a new TimeEntry if no open entry exists
        if not TimeEntry.objects.filter(employee=self, clock_out__isnull=True).exists():
            TimeEntry.objects.create(employee=self, clock_in=timezone.now())
        else:
            raise ValueError("Employee is already clocked in.")

    def clock_out(self):
        # Update the existing open TimeEntry with clock_out time
        open_entry = TimeEntry.objects.filter(employee=self, clock_out__isnull=True).first()
        if open_entry:
            open_entry.clock_out = timezone.now()
            open_entry.save()
        else:
            raise ValueError("Employee is not clocked in.")

    def weekly_hours(self):
        # Calculate hours worked for the current week
        start_of_week = timezone.now().date() - timedelta(days=timezone.now().weekday())
        weekly_entries = TimeEntry.objects.filter(
            employee=self,
            clock_in__date__gte=start_of_week
        )
        total_duration = sum(entry.duration for entry in weekly_entries)
        return total_duration


class TimeEntry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    day = models.DateField(auto_now_add=True)
    
    @property
    def duration(self):
        # Calculate duration in hours if clocked out
        if self.clock_out:
            return (self.clock_out - self.clock_in).total_seconds() / 3600
        else:
            return (timezone.now() - self.clock_in).total_seconds() / 3600
        return 0

    @property
    def total_hours(self):
        if self.clock_in and self.clock_out:
            delta = self.clock_out - self.clock_in
            return delta.total_seconds() / 3600  # returns hours
        return 0  # Return 0 if no clock_out has been made yet

    def __str__(self):
        return f"{self.employee.user.username} - {self.clock_in} to {self.clock_out}"


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Employee.objects.create(user=instance)
        Token.objects.create(user=instance)


def send_verification_email(owner, token):
    activation_url = f"{settings.SITE_URL}{reverse('activate', kwargs={'username': owner.user.username, 'token': token.key})}"
    subject = "Verify your Email"
    message = f"Hello {owner.user.username},\n\nPlease confirm your email to verify ownership of your account.\nClick the link below:\n{activation_url}\n\nThank you!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [owner.email])