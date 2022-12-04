from rest_framework import generics, response, views, status
from rest_framework import filters
from . import models, serializers
from rest_framework_simplejwt import authentication
from rest_framework import permissions
from bases.services.stripe.stripe import stripe_webhook

from accounts.models import BusinessUser
from bases.paginations import LimitOffset8Pagination
# Create your views here.


class ListTransactionAPI(generics.ListAPIView):
    pagination_class = LimitOffset8Pagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    
    serializer_class = serializers.TransactionSerializer

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["timestamp"]

    def get_queryset(self):
        business = BusinessUser.objects.get(user = self.request.user)
        queryset = models.Transactions.objects.filter(receiver = business.id)
        return queryset


class WebhookStripe(views.APIView):

    def post(self, request):
        event = stripe_webhook(request)
        if(type(event).__name__ == "SignatureVerificationError"):
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        if event.type == 'charge.succeeded':
            if(event.data.object.currency == "vnd"):
                data = {
                    "timestamp" : event.created,
                    "stripe_payment": event.data.object.payment_intent,
                    "amount": event.data.object.amount,
                    "order": event.data.object.metadata.order_id,
                    "buyer": event.data.object.metadata.buyer,
                    "receiver": event.data.object.metadata.business
                }
                serializer = serializers.TransactionSerializer(data=data)
                serializer.is_valid()
                serializer.save()
        return response.Response(status=status.HTTP_200_OK)
