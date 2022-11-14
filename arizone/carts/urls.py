from django.urls import path
from . import views
urlpatterns = [
    path('', views.CartAPI.as_view()),
    path('<int:cart_id>/', views.CartDetailAPI.as_view()),
    path('amount/', views.CartAmountAPI.as_view()),
    path('add/', views.AddProductInCartAPI.as_view()),
    path('update/<int:cart_detail_id>/', views.UpdateProductInCartAPI.as_view()),
    path('delete/<int:cart_detail_id>/', views.DeleteProductInCartAPI.as_view()),
]