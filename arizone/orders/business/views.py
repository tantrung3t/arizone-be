from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from bases.permisions import IsBusiness
from bases.paginations import LimitOffset8Pagination
from . import serializers
from .. import models

class ListOrderAPI(generics.ListAPIView):
    pagination_class = LimitOffset8Pagination
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

class DetailOrderAPI(generics.RetrieveAPIView):
    serializer_class = serializers.DetailOrderSerializer
    permission_classes = [IsBusiness]
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        return models.Order.objects.filter(store__user=self.request.user)

class UpdateOrderAPI(generics.UpdateAPIView):
    serializer_class = serializers.UpdateOrderSerializer
    permission_classes = [IsBusiness]
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        return models.Order.objects.filter(store__user=self.request.user)


