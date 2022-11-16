from bases.services.stripe.stripe import stripe_payment_intent_create
from carts.models import Cart
from .. import models
from . import serializers
from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from bases.services.firebase import notification

import stripe
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()
stripe.api_key = settings.STRIPE_SECRET_KEY


class ListOrderAPI(generics.ListAPIView):
    pagination_class = None
    serializer_class = serializers.ListOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['phone']
    filterset_fields = ['status']
    ordering_fields = ['id']

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user)


class CreateOrderAPI(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # serializer = serializers.CreateOrderSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        cart = Cart.objects.get(id=request.data['cart_id'])
        cart.delete()
        order_detail = []
        total = 0
        for product_order in request.data['order']:
            serializer_order_detail = serializers.CreateOrderDetailSerializer(
                data=product_order)
            serializer_order_detail.is_valid(raise_exception=True)
            serializer_order_detail.save()

            if(product_order['sale']):
                total += product_order['sale'] * product_order['quantity']
            else:
                total += product_order['price'] * product_order['quantity']

            order_detail.append(serializer_order_detail.data['id'])

        # print(order_detail)

        data = {
            "user": request.user.id,
            "full_name": request.data['full_name'],
            "phone": request.data['phone'],
            "address": request.data['address'],
            "payment": "cash",
            "status": "pending",
            "total": total,
            "product_detail": order_detail,
            "store": request.data['business'],
        }
        serializer_order = serializers.CreateOrderSerializer(data=data)
        serializer_order.is_valid(raise_exception=True)
        serializer_order.save()
        SendNotify(request.data['business'])
        return response.Response(data=serializer_order.data)


def SendNotify(business):
    queryset = models.BusinessUser.objects.get(id=business)
    notification.send_notify_message(
        user_id=queryset.user.id, msg_title="Arizone", msg_body="Bạn có đơn hàng mới!")


class CreateOrderPaymentOnlineAPI(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        order_detail = []
        total = 0
        for product_order in request.data['order']:
            serializer_order_detail = serializers.CreateOrderDetailSerializer(
                data=product_order)
            serializer_order_detail.is_valid(raise_exception=True)
            serializer_order_detail.save()

            if(product_order['sale']):
                total += product_order['sale'] * product_order['quantity']
            else:
                total += product_order['price'] * product_order['quantity']

            order_detail.append(serializer_order_detail.data['id'])

        # print(order_detail)

        data = {
            "user": request.user.id,
            "full_name": request.data['full_name'],
            "phone": request.data['phone'],
            "address": request.data['address'],
            "payment": "online",
            "status": "pending",
            "total": total,
            "product_detail": order_detail,
            "store": request.data['business'],
        }
        serializer_order = serializers.CreateOrderSerializer(data=data)
        serializer_order.is_valid(raise_exception=True)
        serializer_order.save()

        payment = stripe.PaymentIntent.create(
            amount=total,
            currency="vnd",
            payment_method=request.data['payment'],
            confirm=True,
            payment_method_types=['card'],
            description="Payment for order: " + str(serializer_order.data['id']),
            metadata={
                "order_id": serializer_order.data['id']
            }
        )
        SendNotify(request.data['business'])
        return response.Response(data={
            "client_secret" : payment.client_secret
        })


class CreateOrderSavePaymentOnlineAPI(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        return response.Response(data="payment save")
