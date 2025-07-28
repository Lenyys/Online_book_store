from django.urls import path
from eshop.views import (BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, ImageCreateView,
                         CategoryListView, CategoryUpdateView, CategoryDeleteView, ImageDeleteView,
                         ImageUpdateView, AuthorCreateView, RemoveAuthorFromBook, AuthorUpdateView,
                         StaffBookListView, StaffBookDetailView, AddOrCreateAuthorView, StaffAuthorListView,
                         StaffAuthorDetailView, AuthorDeleteView, AddToCartView, CartDetailView,
                         CategoryCreateView, CategoryDetailView, UpdateCartView, RemoveFromCartView,
                         OrderConfirmationView, CreateOrderView, search_view, autocomplete_search)

urlpatterns = [
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('book_detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),

    path('staff_book_list/', StaffBookListView.as_view(), name='staff_book_list'),
    path('staff_book_detail/<int:pk>/', StaffBookDetailView.as_view(), name='staff_book_detail'),
    path('book_create/', BookCreateView.as_view(), name='book_create'),
    path('book_update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('book_delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

    path('book/<int:pk>/staff_add_author/', AddOrCreateAuthorView.as_view(), name='add_or_create_author'),
    path('book/<int:book_id>/remove_author/<int:author_id>/',RemoveAuthorFromBook.as_view(), name='remove_author'),

    path('staff_autor_list',StaffAuthorListView.as_view(), name="staff_author_list"),
    path('staff_author_detail/<int:pk>/', StaffAuthorDetailView.as_view(), name='staff_author_detail'),
    path('autor_create', AuthorCreateView.as_view()  , name='author_create'),
    path('author_delete/<int:pk>/',AuthorDeleteView.as_view(), name='author_delete'),
    path('book/author_update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),

    path('book/<int:pk>/add_image/', ImageCreateView.as_view(), name='add_image'),
    path('image_delete/<int:pk>/', ImageDeleteView.as_view(), name='image_delete'),
    path('book/<int:book_id>/image_update/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart_detail/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/update/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('order_confirmation/<int:pk>/' ,OrderConfirmationView.as_view() , name='order_confirmation'),

    path('autocomplete-search/', autocomplete_search, name="autocomplete_search"),
    path('search/',search_view ,name="search"),

]
