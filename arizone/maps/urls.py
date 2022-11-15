from django.urls import path

from . import views

urlpatterns = [
    path('', views.GetStoreAPI.as_view())
]