from dataclasses import fields
import imp
from pyexpat import model
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from accounts.models import BusinessUser
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "password",
            "permission",
            "is_active"
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_phone(self, value):
        try:
            int(value)
            if (len(value) != 10):
                raise serializers.ValidationError(
                    "phone number is not available")
            return value
        except:
            raise serializers.ValidationError("phone number is not available")

    def validate_email(self, attrs):
        return attrs.lower()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = [
            "user",
            "address",
            "stripe_connect"
        ]

class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "address",
            "image"
        ]

class BusinessInfoSerializer(serializers.ModelSerializer):
    user = InfoSerializer()
    class Meta:
        model = BusinessUser
        fields = [
            "user",
            "latitude",
            "longitude",
            "address"
        ]