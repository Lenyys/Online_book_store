from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from eshop.forms import ProductForm
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


class ProductCreateView(CreateView):
    model = Product
    template_name = 'eshop/product_create.html'
    form_class = ProductForm
    success_url = reverse_lazy('products_list')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'eshop/product_update.html'
    form_class = ProductForm
    success_url = reverse_lazy('products_list')