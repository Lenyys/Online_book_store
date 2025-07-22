from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Category
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from .forms import CategoryForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from eshop.forms import BookForm, ImageForm, CategoryForm
from eshop.models import Book, Category, Image

# nezapomenout přepnout na strarou stranku home !!!!!!!
def home(request):
    return render(request, 'home.html')


class BookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'

    paginate_by = 10
    ordering = ['-price']


class BookDetailView(DetailView):
    model = Book
    template_name = 'eshop/book_detail.html'
    context_object_name = 'book'


class BookCreateView(CreateView):
    model = Book
    template_name = 'eshop/book_create.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'eshop/book_update.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'eshop/book_delete.html'
    success_url = reverse_lazy('book_list')

class ImageCreateView(CreateView):
    model = Image
    template_name = 'eshop/image_create.html'
    form_class = ImageForm

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.book
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk':self.book.pk})


class CategoryListView(ListView):
    model = Category
    template_name = 'eshop/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eshop/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'eshop/category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'eshop/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')





