from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
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
    search_fields = ['name', 'category__name']
    filterset_fields = ['is_active', "is_block"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return models.Product.objects.filter(
            is_delete=False, created_by=self.request.user)

    def perform_create(self, serializer):
        business = models.BusinessUser.objects.get(user=self.request.user)
        if(business.user.business_status == "pending"):
            serializer.save(created_by=self.request.user,
                            business=business, is_active=False)
        else:
            serializer.save(created_by=self.request.user, business=business)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if(self.request.method == "GET"):
            return serializers.ListProductSerializer
        return super().get_serializer_class()


class RetrieveUpdateDestroyProductAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UpdateProductSerializer
    queryset = models.Product.objects.filter(is_delete=False)
    permission_classes = [IsBusiness]
    authentication_classes = [JWTAuthentication]

    lookup_url_kwarg = "product_id"

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        if(self.request.user.business_status == "pending"):
            serializer.save(is_active=False)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()
