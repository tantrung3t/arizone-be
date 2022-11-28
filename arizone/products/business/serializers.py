from rest_framework import serializers
from .. import models

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "business_status"
        ]
class ListProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = models.Product
        fields = [
            "id",
            "image",
            "name",
            "is_active",
            "is_block",
            "sold",
            "amount",
            "created_by"
        ]


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "name",
            "category",
            "image",
            "price",
            "sale",
            "description",
            "element",
            "type",
            "effect",
            "product_by",
            "is_active",
            "amount"
        ]

class UpdateProductSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    class Meta:
        model = models.Product
        fields = [
            "name",
            "category",
            "image",
            "price",
            "sale",
            "description",
            "element",
            "type",
            "effect",
            "product_by",
            "is_active",
            "is_block",
            "created_by",
            "amount"
        ]

        extra_kwargs = {
            "created_by": {"read_only": True},
        }