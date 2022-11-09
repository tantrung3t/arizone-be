from rest_framework import serializers
from .models import Cart, CartDetail
from accounts.models import CustomUser, BusinessUser
from products.models import Product

class StoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["full_name"]

class BusinessSerializer(serializers.ModelSerializer):
    user = StoreNameSerializer(read_only=True)
    class Meta:
        model = BusinessUser
        fields = [
            "id",
            "user",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "price",
            "sale"
        ]


class CartDetailOnlyReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartDetail
        fields = [
            "id",
            "product",
            "quantity"
        ]
        read_only_fields = [
            "id",
            "product",
            "quantity"
        ]


class ListCartSerializer(serializers.ModelSerializer):
    cart_detail = CartDetailOnlyReadSerializer(many=True)
    business = BusinessSerializer(read_only=True)
    # business = serializers.StringRelatedField()
    class Meta:
        model = Cart
        fields = [
            "id",
            "business",
            "cart_detail"
        ]

class AddProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = [
            "product",
            "quantity"
        ]

class AddCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = [
            "cart",
            "product",
            "quantity"
        ]

class CreateCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "customer",
            "business"
        ]
        read_only_fields = [
            "id"
        ]

class UpdateCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = [
            "id",
            "quantity"
        ]