from rest_framework import serializers
from .. import models


class ListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "id",
            "image",
            "name",
            "is_active",
            "is_block",
            "sold",
            "amount"
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
            "amount"
        ]