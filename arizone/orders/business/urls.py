from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.ListOrderAPI.as_view()),
    path('<int:order_id>/', views.DetailOrderAPI.as_view()),
    path('update/<int:order_id>/', views.UpdateOrderAPI.as_view())
]