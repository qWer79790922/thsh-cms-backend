from django.urls import path
from .views import ContentBlockListView

urlpatterns = [
    path('', ContentBlockListView.as_view(), name='block-list'),
]