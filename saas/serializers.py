from rest_framework import serializers
from django.contrib.auth import get_user_model
from owners.models import Owner
from management.models import Manager
from employees.models import Employee

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_role(self, obj):
        if Owner.objects.filter(user=obj).exists():
            return 'Owner'
        elif Manager.objects.filter(user=obj).exists():
            return 'Manager'
        elif Employee.objects.filter(user=obj).exists():
            return 'Employee'
        return 'Unknown'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
