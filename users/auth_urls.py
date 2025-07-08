from django.urls import path
from .auth_views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('logout/', LogoutView.as_view(), name='jwt-logout'),
    path('refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
]