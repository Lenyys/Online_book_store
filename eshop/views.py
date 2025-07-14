from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Category  # musíš mít oba modely
from .forms import BookForm, CategoryForm  # a oba formuláře


# ---------- Book views ----------

class BookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'eshop/book_detail.html'
    context_object_name = 'book'

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'eshop/book_form.html'
    success_url = reverse_lazy('book-list')

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'eshop/book_form.html'
    success_url = reverse_lazy('book-list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'eshop/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')

# ---------- Category views ----------

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


from django.shortcuts import render  # to už tam možná máš nahoře

def homepage(request):
    return render(request, 'eshop/homepage.html')

