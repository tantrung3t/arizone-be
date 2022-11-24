from logging import raiseExceptions
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt import tokens

from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, BusinessSerializer, BusinessInfoSerializer
from ..models import BusinessUser
# Create your views here.
User = get_user_model()
# Using TokenBlacklistView default
# Using TokenRefreshView default

class BusinessRegisterAPI(APIView):

    def post(self, request, *args, **kwargs):
        request.data['permission'] = "business"
        user = RegisterSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        print(user.data['id'])
        data = {
            "user": user.data['id'],
            "address": request.data["address"]
        }
        serializer = BusinessSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=user.data, status=status.HTTP_201_CREATED)


class BusinessInfoAPI(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        queryset = BusinessUser.objects.get(user=request.user)
        serializer = BusinessInfoSerializer(queryset)
        return Response(serializer.data)

class UpdateInfoAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        business = BusinessUser.objects.get(user=request.user)

        user.full_name = request.data["full_name"]
        user.address = request.data["address"]

        business.latitude = request.data["latitude"]
        business.longitude = request.data["longitude"]
        
        user.save()
        business.save()
        
        return Response(data={
            "message": "OK"
        })