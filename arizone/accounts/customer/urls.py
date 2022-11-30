from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('logout/', views.TokenBlacklistView.as_view(), name='logout'),
    path('refresh-token/', views.TokenRefreshView.as_view(), name='refresh-token'),
    path('user/', views.UserAPI.as_view(), name="user"),
    path('user/profile/', views.UserProfileAPI.as_view(), name="user-profile"),
    path('user/profile/image/', views.ImageUserProfileAPI.as_view(), name="user-profile"),
    path('store/<int:store_id>', views.StoreAPI.as_view()),
    path('address/', views.AddressAPI.as_view()),
    path('address/<int:address_id>/', views.DestroyAddressAPI.as_view()),
]