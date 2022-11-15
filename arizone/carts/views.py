from rest_framework import generics, views
from rest_framework import response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import serializers, models
from products.models import Product
# Create your views here.


class CartAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.ListCartSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(customer=self.request.user)


class CartDetailAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.ListCartSerializer
    lookup_url_kwarg = "cart_id"

    def get_queryset(self):
        return models.Cart.objects.filter(customer=self.request.user)


class AddProductInCartAPI(views.APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = serializers.AddProductInCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query_product = Product.objects.filter(id=request.data['product'])

        try:
            query_cart = models.Cart.objects.get(
                customer=request.user, business=query_product[0].business)

            try:

                query_product_in_cart = models.CartDetail.objects.get(
                    cart=query_cart.id, product=request.data['product'])

                query_product_in_cart.quantity += request.data['quantity']
                query_product_in_cart.save()
            except:
                data = {
                    "cart": query_cart.id,
                    "product": request.data['product'],
                    "quantity": request.data['quantity']
                }
                serializer_cart_detail = serializers.AddCartDetailSerializer(
                    data=data)
                serializer_cart_detail.is_valid(raise_exception=True)
                serializer_cart_detail.save()
        except:
            cart_id = self.create_cart(
                request.user.id, query_product[0].business.id)
            data = {
                "cart": cart_id,
                "product": request.data['product'],
                "quantity": request.data['quantity']
            }
            serializer_cart_detail = serializers.AddCartDetailSerializer(
                data=data)
            serializer_cart_detail.is_valid(raise_exception=True)
            serializer_cart_detail.save()

        return response.Response(data=request.data, status=status.HTTP_201_CREATED)

    def create_cart(self, user_id, business_id):
        data = {
            "customer": user_id,
            "business": business_id
        }
        serializer = serializers.CreateCartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer.data['id']


class UpdateProductInCartAPI(generics.UpdateAPIView):
    queryset = models.CartDetail.objects.all()
    serializer_class = serializers.UpdateCartDetailSerializer
    lookup_url_kwarg = "cart_detail_id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.quantity += request.data['quantity']
        instance.save()
        return response.Response(data={
            "status": "success"
        })

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)


class DeleteProductInCartAPI(generics.DestroyAPIView):
    queryset = models.CartDetail.objects.all()
    serializer_class = serializers.UpdateCartDetailSerializer
    lookup_url_kwarg = "cart_detail_id"


class CartAmountAPI(generics.ListAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.ListCartSerializer

    def get_queryset(self):
        return models.Cart.objects.filter(customer=self.request.user)

    def list(self, request, *args, **kwargs):
        cart = super().list(request, *args, **kwargs)
        amount = 0
        for x in cart.data:
            for y in x['cart_detail']:
                amount += y['quantity']
        return response.Response(data={
            "amount": amount
        })
