from django.urls import path
from .views import MeView, RegisterView

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('', RegisterView.as_view(), name='register'),
]