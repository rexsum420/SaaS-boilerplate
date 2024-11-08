from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.conf import settings
from saas.fields import SSNField


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=24, blank=True, null=True)
    last_name = models.CharField(max_length=24, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    last_active = models.CharField(max_length=512, blank=True, null=True)
    ssn = SSNField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.username
