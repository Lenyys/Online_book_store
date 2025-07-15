

from django.urls import path
from eshop.views import (BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, ImageCreateView,
                         CategoryListView, CategoryUpdateView, CategoryDeleteView, ImageListView, ImageDeleteView,
                         ImageUpdateView, AuthorCreateView, AuthorListView, RemoveAuthorFromBook, AuthorUpdateView,
                         )

urlpatterns = [

    path('book_list/', BookListView.as_view(), name='book_list'),
    path('book_detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book_create/', BookCreateView.as_view(), name='book_create'),
    path('book_update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('book_delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('book/<int:pk>/add_image/', ImageCreateView.as_view(), name='add_image'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('book/<int:pk>/image_list/',ImageListView.as_view() , name='book_image_list'),
    path('image_delete/<int:pk>/', ImageDeleteView.as_view(), name='image_delete'),
    path('book/<int:book_id>/image_update/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),
    path('book/<int:pk>/add_author/', AuthorCreateView.as_view()  , name='add_author'),

    path('book/<int:pk>/author_list/',AuthorListView.as_view() , name='book_author_list'),

    path('book/<int:book_id>/remove_author/<int:author_id>/',RemoveAuthorFromBook.as_view(), name='remove_author'),
    path('book/author_update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),




]