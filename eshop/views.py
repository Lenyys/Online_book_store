from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from eshop.forms import BookForm
from eshop.models import Book


# Create your views here.


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
