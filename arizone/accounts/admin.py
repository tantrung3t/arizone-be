from django.contrib import admin
from .models import CustomUser, Permission, BusinessUser
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Permission)
admin.site.register(BusinessUser)