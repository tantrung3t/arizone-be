
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
import uuid
# Create your models here.
# custom user model


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Permission(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'permissions'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.EmailField(_('email address'), unique=True)
    address = models.TextField(null=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10)
    stripe_customer = models.CharField(max_length=30, null=True, blank=True)
    permission = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=255, blank=True)
    block_at = models.DateTimeField(blank=True, null=True)
    block_by = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(null=True, upload_to="images/profile/")
    business_status = models.CharField(max_length=255, null=True, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    REQUIRED_FIELDS = ["phone"]
    USERNAME_FIELD = "email"

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.email

class BusinessUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="business_user")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, default=105)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, default=10)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=True)
    rating = models.FloatField(default=0)
    amount_product = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    stripe_connect = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class DeliveryAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Pin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    pin = models.IntegerField()
    expired = models.CharField(null=True, max_length=255)

    def __str__(self) -> str:
        return str(self.user) + " " + str(self.pin)