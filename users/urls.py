from django.urls import path
from .views import MeView, RegisterView, ChangePasswordView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('', RegisterView.as_view(), name='register'),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]