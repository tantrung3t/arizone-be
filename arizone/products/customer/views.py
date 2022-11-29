from rest_framework import generics
from bases.paginations import LimitOffset16Pagination
from rest_framework.response import Response
from . import serializers
from .. import models
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import BusinessUser

class ListCategoryAPI(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    pagination_class = None

class ListProductAPI(generics.ListAPIView):
    serializer_class = serializers.ListProductSerializer
    queryset = models.Product.objects.filter(
        is_active=True, is_delete=False, is_block=False, created_by__business_status="active")
    pagination_class = LimitOffset16Pagination

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'product_by']
    filterset_fields = ['category']
    ordering_fields = ["average_rating"]


class DetailProductAPI(generics.RetrieveAPIView):
    lookup_url_kwarg = 'product_id'
    queryset = models.Product.objects.filter(
        is_active=True, is_delete=False, is_block=False, created_by__business_status="active")
    serializer_class = serializers.DetailProductSerializer

    def get_store(self, request, *args, **kwargs):
        queryset = BusinessUser.objects.get(user=self.user_id)
        serializer = serializers.StoreSerializer(queryset)
        return Response(serializer.data)
