from django.db import models

# Create your models here.

class Transactions(models.Model):
    timestamp = models.CharField(max_length=20)
    stripe_payment = models.CharField(max_length=50, null=True)
    amount = models.CharField(max_length=20)
    order = models.CharField(max_length=10)
    buyer = models.CharField(max_length=255)
    receiver = models.CharField(max_length=10)