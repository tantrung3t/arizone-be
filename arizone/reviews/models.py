from django.db import models
from products.models import Product
from accounts.models import CustomUser
# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    star = models.FloatField()
    content = models.TextField()