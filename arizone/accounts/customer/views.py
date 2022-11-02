
from os import stat
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
from .serializers import UserProfileSerializer, UserImageProfileSerializer
from django.contrib.auth import get_user_model
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
        return Response(data={
            "permission": request.user.permission,
            "full_name": request.user.full_name
        },
            status=status.HTTP_200_OK)


class UserProfileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def get(self, request):
        queryset = User.objects.get(email=request.user)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)

    def post(self, request):
        user_profile = User.objects.get(email=request.user)
        serializer = UserProfileSerializer(instance=user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)

class ImageUserProfileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

    def post(self, request):
        user_profile = User.objects.get(email=request.user)
        serializer = UserImageProfileSerializer(instance=user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)