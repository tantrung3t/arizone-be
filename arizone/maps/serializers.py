from rest_framework import serializers
from accounts.models import CustomUser, BusinessUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "full_name",
            "image"
        ]

class GetStoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BusinessUser
        fields = [
            "id",
            "user",
            "longitude",
            "latitude"
        ]