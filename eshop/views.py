from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from eshop.forms import BookForm, ImageForm
from eshop.models import Book, Category, Image


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




########################################################################################

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'eshop/category_list.html', {'categories': categories})


from django.shortcuts import get_object_or_404, redirect
from .forms import CategoryForm

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'eshop/category_form.html', {'form': form})


from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'eshop/category_confirm_delete.html', {'category': category})
