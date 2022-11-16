from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import serializers
from fcm_django.models import FCMDevice
from bases.permisions import IsBusiness
from accounts.models import BusinessUser

# Create your views here.


class TokenDeviceAPI(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsBusiness]

    def post(self, request):

        try:
            instance = FCMDevice.objects.get(user=request.user.id)
            instance.registration_id = request.data['token']
            instance.active = True
            instance.save()
            return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)
        except:
            queryset = FCMDevice.objects.filter(user=request.user.id)
            if(len(queryset) == 0):
                data = {
                    "user": request.user.id,
                    "registration_id": request.data['token']
                }
                serializer = serializers.DeviceSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return response.Response(data={"message": "ok"}, status=status.HTTP_201_CREATED)
            else:
                return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            instance = FCMDevice.objects.get(user=request.user.id)
            instance.active = False
            instance.save()
        except:
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
