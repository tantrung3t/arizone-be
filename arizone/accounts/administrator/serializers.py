
from dataclasses import fields
from pyexpat import model
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import BusinessUser
User = get_user_model()


class UpdateBusinessUserAPI(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "is_active",
        ]
        
        extra_kwargs = {
            "id": {"read_only": True},
            "full_name": {"read_only": True},
            "phone": {"read_only": True},
            "email": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "is_active",
        ]
