
from django.urls import path
from eshop.views import (BookListView, EBookListView, AudioBookListView, BookDetailView, BookCreateView, BookUpdateView,
                         BookDeleteView, ImageCreateView,

                         CategoryListView, StaffCategoryListView, StaffCategoryDeleteView, StaffCategoryDetailView,
                         StaffCategoryUpdateView, StaffCategoryCreateView,

                         ImageDeleteView,
                         ImageUpdateView, AuthorCreateView, RemoveAuthorFromBook, AuthorUpdateView,
                         StaffBookListView, StaffBookDetailView, AddOrCreateAuthorView, StaffAuthorListView,
                         StaffAuthorDetailView, AuthorDeleteView, AddToCartView, CartDetailView,
                         UpdateCartView, RemoveFromCartView,
                         OrderConfirmationView, CreateOrderView, FavoriteBookView, FavoriteBooksListView,
                         search_view, autocomplete_search, FavoriteBookRemoveFromFavoritesList)


urlpatterns = [
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('ebooks/', EBookListView.as_view(), name='e_book_list'),
    path('audiobooks/', AudioBookListView.as_view(), name='audio_book_list'),
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

    # Veřejné pouze na čtení (list a detail)
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Správa kategorií ve staff rozhraní (pouze staff users)
    path('staff_category_list/', StaffCategoryListView.as_view(), name='staff_category_list'),
    path('staff_category_detail/<int:pk>/', StaffCategoryDetailView.as_view(), name='staff_category_detail'),
    path('staff_category_edit/<int:pk>/', StaffCategoryUpdateView.as_view(), name='staff_category_edit'),
    path('staff_category_delete/<int:pk>/', StaffCategoryDeleteView.as_view(), name='staff_category_delete'),
    path('staff_category_create/', StaffCategoryCreateView.as_view(), name='staff_category_create'),


    path('cart/add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart_detail/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/update/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('order_confirmation/<int:pk>/' ,OrderConfirmationView.as_view() , name='order_confirmation'),

    path('book/favorite_book/<int:book_id>/', FavoriteBookView.as_view(), name='favorite_book'),
    path('books/favorites/', FavoriteBooksListView.as_view(), name='user_favorite_books'),
    path('book/favorite_remove/<int:book_id>/', FavoriteBookRemoveFromFavoritesList.as_view(), name='favorite_remove'),

    path('autocomplete-search/', autocomplete_search, name="autocomplete_search"),
    path('search/',search_view ,name="search"),

]
