from django.contrib import admin
from .models import CustomUser, Permission, BusinessUser, DeliveryAddress, Pin
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Permission)
admin.site.register(BusinessUser)
admin.site.register(DeliveryAddress)
admin.site.register(Pin)