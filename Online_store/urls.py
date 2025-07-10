"""
URL configuration for Online_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from eshop.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('eshop/book_list/', BookListView.as_view(), name='book_list'),
    path('eshop/book_detail/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('eshop/book_create/', BookCreateView.as_view(), name='book_create'),
    path('eshop/book_update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('eshop/book_delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

    path('', include('eshop.urls')),

    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-edit'),
    # path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete')

]
