

from django.urls import path
from eshop.views import (BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, ImageCreateView,
                         CategoryListView, CategoryUpdateView, CategoryDeleteView,
                         )

urlpatterns = [

    path('book_list/', BookListView.as_view(), name='book_list'),
    path('book_detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book_create/', BookCreateView.as_view(), name='book_create'),
    path('book_update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('book_delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('book/<int:pk>/add-image/', ImageCreateView.as_view(), name='add_image'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

]