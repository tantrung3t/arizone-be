from rest_framework import generics
from bases.paginations import LimitOffset8Pagination
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from .. import models
from accounts.models import BusinessUser


class ListProductAPI(generics.ListAPIView):
    serializer_class = serializers.ListProductSerializer
    queryset = models.Product.objects.filter(is_delete=False)
    pagination_class = LimitOffset8Pagination
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['is_active', "is_block"]
    ordering_fields = ["created_at"]


