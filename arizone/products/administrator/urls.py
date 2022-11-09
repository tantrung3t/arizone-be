from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.ListProductAPI.as_view()),
    path('update/<int:product_id>/', views.UpdateProductAPI.as_view()),
]