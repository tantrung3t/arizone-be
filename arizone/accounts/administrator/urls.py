from django.urls import path, include
from . import views

urlpatterns = [
    path('user/list/', views.ListBusinessUserAPI.as_view(), name='user_list'),
    path('user/<str:user_id>/', views.ActiveBusinessUserAPI.as_view()),
]