from rest_framework import serializers
from fcm_django.models import FCMDevice


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = [
            "user",
            "registration_id"
        ]
