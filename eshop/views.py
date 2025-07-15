from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View

from .models import Category, Autor
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from .forms import CategoryForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from eshop.forms import BookForm, ImageForm, CategoryForm, AuthorForm
from eshop.models import Book, Category, Image


def home(request):
    return render(request, 'home.html')


class BookListView(ListView):
    model = Book
    template_name = 'eshop/book_list.html'
    context_object_name = 'books'

    paginate_by = 10
    ordering = ['-price']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = get_object_or_404(Category, id=category_id)

        return context



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context

class ImageUpdateView(UpdateView):
    model = Image
    template_name = 'eshop/image_update.html'
    form_class = ImageForm

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('book_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.book
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        print("mazání ok , přesměrování na:", next_url )
        return next_url or reverse_lazy('book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context


class ImageListView(ListView):
    model = Image
    template_name = 'eshop/book_image_list.html'
    context_object_name = 'images'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Image.objects.filter(product=self.book)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context


class ImageDeleteView(DeleteView):
    model = Image
    template_name = 'eshop/image_delete.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        print("mazání ok , přesměrování na:", next_url )
        return next_url or reverse_lazy('book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context


class AuthorCreateView(CreateView):
    model = Autor
    template_name = 'eshop/author_create.html'
    form_class = AuthorForm

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.books.add(self.book)
        return response

    def get_success_url(self):
        return reverse('book_detail', kwargs={'pk': self.book.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context



class AuthorUpdateView(UpdateView):
    model = Autor
    template_name = 'eshop/author_update.html'
    form_class = AuthorForm

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        print("mazání ok , přesměrování na:", next_url )
        return next_url or reverse_lazy('book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context


class AuthorListView(ListView):
    model = Autor
    template_name = 'eshop/book_autor_list.html'
    context_object_name = 'authors'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Autor.objects.filter(books=self.book)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book
        return context


class AuthorDeleteView(DeleteView):
    model = Autor
    template_name = 'eshop/author_delete.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        print("mazání ok , přesměrování na:", next_url )
        return next_url or reverse_lazy('book_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_url'] = self.request.GET.get('next','/')
        return context

class RemoveAuthorFromBook(View):
    template_name = 'eshop/remove_author_from_book.html'

    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['book_id'])
        self.author = get_object_or_404(Autor, pk=kwargs['author_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'book': self.book,
            'author': self.author,
            'next': request.GET.get('next', reverse('book_detail', kwargs={'pk': self.book.pk}))
        })

    def post(self, request, *args, **kwargs):
        self.book.autor.remove(self.author)
        next_url = request.POST.get('next') or reverse('book_detail', kwargs={'pk': self.book.pk})
        return redirect(next_url)


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





