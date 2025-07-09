from django.urls import path
from .views import ContentBlockListView, ContentBlockCreateView, ContentBlockUpdateView

urlpatterns = [
    path('', ContentBlockListView.as_view(), name='content-block-list'),
    path('create/', ContentBlockCreateView.as_view(), name='content-block-create'),
    path('<int:pk>/', ContentBlockUpdateView.as_view(), name='content-block-update'),
]