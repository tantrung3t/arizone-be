from django.db import models
from accounts.models import CustomUser, BusinessUser
from products.models import Product
# Create your models here.


class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    business = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("customer", "business"),)

    def __str__(self) -> str:
        return str(self.customer) + " + " + str(self.business)


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_detail")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = (("cart", "product"),)

    def __str__(self) -> str:
        return str(self.cart) + " + " + str(self.product) + " + " + str(self.quantity)
