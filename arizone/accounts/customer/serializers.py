from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .. import models
User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate_email(self, email):
        return email.lower()

    def validate(self, attrs):
        data = super().validate(attrs)
        if(self.user.permission == ""):
            data["permission"] = "admin"
        else:
            data["permission"] = self.user.permission
        data["active"] = self.user.is_active
        return data

    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        # ...
        return token


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "email",
            "password",
            "permission",
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "permission",
            "phone",
            "address",
            "image",
            "stripe_customer"
        ]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "phone",
            "birthday",
            "sex",
            "image"
        ]
        extra_kwargs = {
            'image': {'read_only': True},
            'email': {'read_only': True},
        }

class UserImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "image"
        ]




class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.BusinessUser
        fields = [
            "id",
            "user",
            "longitude",
            "latitude"
        ]