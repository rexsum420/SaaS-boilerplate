from rest_framework import serializers
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['user', 'email', 'first_name', 'last_name', 'phone_number', 'ssn', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['user'].username,
            email=validated_data['user'].email,
            password=password
        )
        owner = Employee.objects.create(user=user, **validated_data)
        return owner