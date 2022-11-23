from django.shortcuts import render
from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from . import models, serializers
# Create your views here.

from products.ultis import add_rating

class CreateReviewAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.CreateReviewSerializer
    queryset = models.Review.objects.all()
    
    def perform_create(self, serializer):
        add_rating(self.request.data['star'], self.request.data['product'])
        serializer.save(user=self.request.user)

class ListReviewAPI(generics.ListAPIView):

    serializer_class = serializers.ListReviewSerializer
    lookup_url_kwarg = "product_id"

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        return models.Review.objects.filter(product=uid)