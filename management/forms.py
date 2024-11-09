from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Manager
from django.contrib.auth.models import User
from employees.models import Employee

class ManagerForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset = User.objects.exclude(id__in=Manager.objects.values('user')).exclude(id__in=Employee.objects.values('user')),

        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ssn = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'ssnInput'}))
    class Meta:
        model = Manager
        fields = ('user', 'first_name', 'last_name', 'email', 'phone_number', 'ssn', 'pin')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pin': forms.TextInput(attrs={'class': 'form-control'}),
        }
