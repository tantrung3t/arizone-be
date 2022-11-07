from django.urls import path, include
from . import views

urlpatterns = [
    path('list/', views.ListProductAPI.as_view())
]