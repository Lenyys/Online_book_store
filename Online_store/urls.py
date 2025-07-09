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
from django.urls import path

from eshop.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('eshop/products_list/', ProductListView.as_view(), name='products_list'),
    path('eshop/product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('eshop/product_create/', ProductCreateView.as_view(), name='product_create'),
    path('eshop/product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
]
