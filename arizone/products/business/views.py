from rest_framework import generics
from bases.paginations import LimitOffset8Pagination
from bases.permisions import IsBusiness
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from .. import models
from accounts.models import BusinessUser


class ListCreateProductAPI(generics.ListCreateAPIView):
    serializer_class = serializers.CreateProductSerializer
    queryset = models.Product.objects.filter(is_delete=False)
    pagination_class = LimitOffset8Pagination
    permission_classes = [IsBusiness]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['is_active', "is_block"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return models.Product.objects.filter(
            is_delete=False, created_by=self.request.user)

    def perform_create(self, serializer):
        business = models.BusinessUser.objects.get(user=self.request.user)
        serializer.save(created_by=self.request.user, business=business)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if(self.request.method == "GET"):
            return serializers.ListProductSerializer
        return super().get_serializer_class()
