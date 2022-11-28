from logging import raiseExceptions
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens, authentication
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model
from ..models import BusinessUser

from .serializers import UserSerializer, UpdateBusinessUserAPI

from bases.paginations import LimitOffset8Pagination
User = get_user_model()

class ListBusinessUserAPI(generics.ListAPIView):
    pagination_class = LimitOffset8Pagination
    queryset = User.objects.filter(permission = "business")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name','email','phone']
    filterset_fields = ['is_active', "business_status"]
    ordering_fields = [
        "date_joined"
        ]

class ActiveBusinessUserAPI(generics.UpdateAPIView):
    queryset = User.objects.filter(permission = "business")
    serializer_class = UpdateBusinessUserAPI
    lookup_url_kwarg = 'user_id'
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.JWTAuthentication]
