from rest_framework import serializers
from .. import models
from products.models import Product


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

class ListOrderSerializer(serializers.ModelSerializer):
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
            "product_detail",
            "store",
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
            "product_detail",
            "store",
        ]
