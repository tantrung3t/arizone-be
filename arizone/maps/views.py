from django.shortcuts import render
from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import filters
from . import models, serializers
from accounts.models import BusinessUser

# Create your views here.

class GetStoreAPI(views.APIView):

    def post(self, request):
        queryset = BusinessUser.objects.all()
        serializer = serializers.GetStoreSerializer(queryset, many=True)
        return response.Response(data=serializer.data)