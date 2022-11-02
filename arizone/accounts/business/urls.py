from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.BusinessRegisterAPI.as_view(), name='business_register'),
]