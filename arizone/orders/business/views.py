from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from bases.permisions import IsBusiness
from . import serializers
from .. import models

class ListOrderAPI(generics.ListAPIView):
    serializer_class = serializers.ListOrderSerializer
    permission_classes = [IsBusiness]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['phone']
    filterset_fields = ['status']
    ordering_fields = ['id']

    def get_queryset(self):
        return models.Order.objects.filter(store__user=self.request.user)