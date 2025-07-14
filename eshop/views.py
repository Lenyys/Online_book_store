from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Category
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from .forms import CategoryForm


def home(request):
    return render(request, 'home.html')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'eshop/category_list.html', {'categories': categories})


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


@require_http_methods(["GET", "POST"])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'eshop/category_confirm_delete.html', {'category': category})
