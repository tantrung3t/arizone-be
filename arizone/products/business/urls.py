from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ListCreateProductAPI.as_view()),
    path('<int:product_id>', views.RetrieveUpdateDestroyProductAPI.as_view())
]