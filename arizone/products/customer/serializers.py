from rest_framework import serializers
from django.contrib.auth import get_user_model
from .. import models
from accounts.models import BusinessUser

User = get_user_model()


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "id",
            "name",
            "price",
            "sale",
            "image",
            "average_rating"
        ]


class NameStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "created", "image"]


class StoreSerializer(serializers.ModelSerializer):
    user = NameStoreSerializer()

    class Meta:
        model = BusinessUser
        fields = [
            "user",
            "address",
            "rating",
            "amount_product",
            "sold"
        ]


class DetailProductSerializer(serializers.ModelSerializer):
    business = StoreSerializer()
    class Meta:
        model = models.Product
        fields = [
            "name",
            "price",
            "sale",
            "image",
            "average_rating",
            "amount_rating",
            "description",
            "element",
            "type",
            "effect",
            "product_by",
            "business"
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"