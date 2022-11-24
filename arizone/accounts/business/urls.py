from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.BusinessRegisterAPI.as_view(), name='business_register'),
    path('profile/', views.BusinessInfoAPI.as_view()),
    path('profile/update/', views.UpdateInfoAPI.as_view())
]