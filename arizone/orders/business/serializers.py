from rest_framework import serializers
from .. import models
from products.models import Product
from accounts.models import CustomUser, BusinessUser

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            "status"
        ]

class DetailProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image"
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    product = DetailProductSerializer()

    class Meta:
        model = models.OrderDetail
        fields = [
            "id",
            "product",
            "price",
            "sale",
            "quantity"
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "full_name"
        ]
class StoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BusinessUser
        fields = [
            "id",
            "user"
        ]

class ListOrderSerializer(serializers.ModelSerializer):
    # product_detail = OrderDetailSerializer(many=True)
    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "address",
            "payment",
            "status",
            "total",
            # "product_detail"

        ]

class DetailOrderSerializer(serializers.ModelSerializer):
    product_detail = OrderDetailSerializer(many=True)
    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "address",
            "payment",
            "status",
            "total",
            "product_detail"
        ]
class CreateOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderDetail
        fields = [
            "id",
            "product",
            "price",
            "sale",
            "quantity"
        ]


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = [
            "id",
            "user",
            "full_name",
            "phone",
            "address",
            "payment",
            "status",
            "total",
            "product_detail",
            "store",
        ]
