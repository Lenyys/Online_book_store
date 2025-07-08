from django.shortcuts import render
from django.views.generic import ListView, DetailView

from eshop.models import Product


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'eshop/products_list.html'
    context_object_name = 'products'

    paginate_by = 10
    ordering = ['-price']

class ProductDetailView(DetailView):
    model = Product
    template_name = 'eshop/product_detail.html'
    context_object_name = 'product'
