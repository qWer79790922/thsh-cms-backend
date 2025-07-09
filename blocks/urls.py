from django.urls import path
from .views import ContentBlockListView, ContentBlockCreateView

urlpatterns = [
    path('', ContentBlockListView.as_view(), name='content-block-list'),
    path('create/', ContentBlockCreateView.as_view(), name='content-block-create'),
]