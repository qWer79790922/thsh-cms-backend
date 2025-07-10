from django.urls import path
from .views import (
    ContentBlockListView,
    ContentBlockCreateView,
    ContentBlockUpdateView,
    ContentBlockBatchCreateView,
    ContentBlockBatchUpdateView,
    ContentBlockPreviewView,
)

urlpatterns = [
    path('', ContentBlockListView.as_view(), name='content-block-list'),
    path('create/', ContentBlockCreateView.as_view(), name='content-block-create'),
    path('<int:pk>/', ContentBlockUpdateView.as_view(), name='content-block-update'),
    path('batch-create/', ContentBlockBatchCreateView.as_view(), name='content-block-batch-create'),
    path('batch-update/', ContentBlockBatchUpdateView.as_view(), name='content-block-batch-update'),
    path('preview/', ContentBlockPreviewView.as_view(), name='content-block-preview'),
]