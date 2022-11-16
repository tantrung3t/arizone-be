from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.ListOrderAPI.as_view()),
    path('create/cash/', views.CreateOrderAPI.as_view()),
    path('create/online/', views.CreateOrderAPI.as_view())
]