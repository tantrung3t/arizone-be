from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import serializers
from .. import models


class ListOrderAPI(generics.ListAPIView):
    pagination_class = None
    serializer_class = serializers.ListOrderSerializer
    queryset = models.Order.objects.all()


class CreateOrderAPI(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # serializer = serializers.CreateOrderSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)

        order_detail = []

        for product_order in request.data['order']:
            serializer_order_detail = serializers.CreateOrderDetailSerializer(
                data=product_order)
            serializer_order_detail.is_valid(raise_exception=True)
            serializer_order_detail.save()
            order_detail.append(serializer_order_detail.data['id'])

        print(order_detail)

        data = {
            "user": request.user.id,
            "full_name": request.data['full_name'],
            "phone":request.data['phone'],
            "address":request.data['address'],
            "payment": "cash",
            "status": "pending",
            "product_detail": order_detail,
            "store": request.data['business'],
        }

        serializer_order = serializers.CreateOrderSerializer(data=data)
        serializer_order.is_valid(raise_exception=True)
        serializer_order.save()
        return response.Response(data=serializer_order.data)
