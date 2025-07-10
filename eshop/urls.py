from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category-edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
]
