from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.ListProductAPI.as_view()),
    path('<int:product_id>/', views.DetailProductAPI.as_view()),
    path('category/', views.ListCategoryAPI.as_view()),
]