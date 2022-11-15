from django.db import models
from products.models import Product
from accounts.models import CustomUser, BusinessUser
# Create your models here.


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    sale = models.IntegerField()
    quantity = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)
    status = models.CharField(default="pending", max_length=50)
    product_detail = models.ManyToManyField(OrderDetail)
    total = models.IntegerField(default=0)
    store = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)