from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.ListOrderAPI.as_view()),
]