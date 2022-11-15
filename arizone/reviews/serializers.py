from rest_framework import serializers
from .models import Review
from accounts.models import CustomUser, BusinessUser
from products.models import Product

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "product",
            "star",
            "content"
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "image"
        ]

class ListReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Review
        fields = [
            "user",
            "product",
            "star",
            "content"
        ]