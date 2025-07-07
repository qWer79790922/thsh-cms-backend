from django.urls import path
from .auth_views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]