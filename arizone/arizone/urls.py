"""arizone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-site/', admin.site.urls),

    path('', include('accounts.customer.urls')),
    path('business/', include('accounts.business.urls')),
    path('admin/', include('accounts.administrator.urls')),

    path('product/', include('products.customer.urls')),
    path('business/product/', include('products.business.urls')),
    path('admin/product/', include('products.administrator.urls')),
    
    path('cart/', include('carts.urls')),

    path('order/', include('orders.customer.urls')),
    path('business/order/', include('orders.business.urls')),

    path('review/', include('reviews.urls')),

    path('map/', include('maps.urls')),

    path('device/', include('devices.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
