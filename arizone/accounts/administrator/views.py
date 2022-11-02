from logging import raiseExceptions
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens, authentication


from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UpdateBusinessUserAPI
User = get_user_model()

class ListBusinessUserAPI(generics.ListAPIView):
    queryset = User.objects.filter(permission = "business")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.JWTAuthentication]

class ActiveBusinessUserAPI(generics.UpdateAPIView):
    queryset = User.objects.filter(permission = "business")
    serializer_class = UpdateBusinessUserAPI
    lookup_url_kwarg = 'user_id'
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.JWTAuthentication]