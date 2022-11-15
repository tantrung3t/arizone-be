from django.urls import path
from . import views
urlpatterns = [
    path('', views.CreateReviewAPI.as_view()),
    path('<int:product_id>/', views.ListReviewAPI.as_view()),
]