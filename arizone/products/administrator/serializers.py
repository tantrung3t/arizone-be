from rest_framework import serializers
from accounts.models import CustomUser
from .. import models


class StoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["full_name"]

class ListProductSerializer(serializers.ModelSerializer):
    created_by = StoreNameSerializer()
    class Meta:
        model = models.Product
        fields = [
            "id",
            "image",
            "name",
            "is_active",
            "is_block",
            "created_by"
        ]

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            "is_block",
        ]