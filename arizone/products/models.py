from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser, BusinessUser
# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to="images/product/")
    amount_rating = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    price = models.IntegerField()
    sale = models.IntegerField(default=0)
    description = models.TextField()
    element = models.TextField()
    type = models.TextField()
    effect = models.TextField()
    product_by = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name
