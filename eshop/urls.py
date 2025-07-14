from django.urls import path
from .views import (
    homepage,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
]
