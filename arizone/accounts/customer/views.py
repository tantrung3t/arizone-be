
from .. import models
import random
from datetime import datetime
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from .serializers import MyTokenObtainPairSerializer
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from .serializers import UserProfileSerializer, UserImageProfileSerializer, UserSerializer, StoreSerializer, AddressSerializer, ChangePasswordWithPinSerializer, ForgotPasswordSerializer, PinSerializer
from django.contrib.auth import get_user_model
from accounts.models import Pin

# Create your views here.
User = get_user_model()
# Using TokenBlacklistView default
# Using TokenRefreshView default


class LoginAPI(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # request.data['email'] = request.data.get('email').lower()
        return super().post(request, *args, **kwargs)


class RegisterAPI(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # request.data['email'] = request.data.get('email').lower()
        request.data['permission'] = "customer"
        return super().create(request, *args, **kwargs)


class UserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get(self, request):
        queryset = User.objects.get(email=request.user)
        serializer = UserSerializer(queryset)
        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)


class UserProfileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get(self, request):
        queryset = User.objects.get(email=request.user)
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def post(self, request):
        user_profile = User.objects.get(email=request.user)
        serializer = UserProfileSerializer(
            instance=user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class ImageUserProfileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def post(self, request):
        user_profile = User.objects.get(email=request.user)
        serializer = UserImageProfileSerializer(
            instance=user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)


class StoreAPI(generics.RetrieveAPIView):

    queryset = models.BusinessUser.objects.all()
    serializer_class = StoreSerializer
    lookup_url_kwarg = "store_id"


class AddressAPI(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = AddressSerializer

    pagination_class = None

    def get_queryset(self):
        return models.DeliveryAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DestroyAddressAPI(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    serializer_class = AddressSerializer
    lookup_url_kwarg = "address_id"

    def get_queryset(self):
        return models.DeliveryAddress.objects.filter(user=self.request.user)


class ForgotPasswordApiView(APIView):
    def create_pin(self, user):
        pin = random.randint(100000, 999999)
        dt = datetime.now()
        ts = int(datetime.timestamp(dt))
        expired = ts + (60 * 10)
        data = {
            'user': user.id,
            'pin': pin,
            'expired': expired
        }
        pin_user = Pin.objects.filter(user=user.id)
        if(pin_user.exists()):
            serializer = PinSerializer(
                instance=pin_user[0], data=data)
        else:
            serializer = PinSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return pin

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=request.data["email"].lower())
        pin_code = self.create_pin(user)
        # html_content = render_to_string(
        #     "index.html", {'pin': pin_code})
        # send_background_mail.delay(request.data["email"], html_content)
        return Response({"message": "Send email completed"}, status=status.HTTP_200_OK)


class ChangePasswordWithPINApiView(APIView):

    def disable_pin(self):
        self.pin.delete()

    def post(self, request):
        serializer = ChangePasswordWithPinSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        self.user = get_object_or_404(
            User, email=request.data['email'].lower())
        self.pin = get_object_or_404(Pin, user=self.user.id)

        """
        check if the user's PIN code input pin is correct
        and check expired PIN code
        """

        dt = datetime.now()
        ts = int(datetime.timestamp(dt))

        if (int(request.data['pin']) == int(self.pin.pin) and int(self.pin.expired) > ts):
            self.user.set_password(request.data['new_password'])
            self.user.save()
            self.disable_pin()
            return Response(data={"detail": "Change password is success"}, status=status.HTTP_200_OK)
        else:
            return Response(data={
                "error": "PIN",
                "message": "Invalid PIN code or expired"
            }, status=status.HTTP_400_BAD_REQUEST)
