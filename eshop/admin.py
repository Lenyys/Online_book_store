from django.contrib import admin
from eshop.models import Category, Book, SelectedProduct, Image, Order, Cart, Autor
from .models import Book
from mptt.admin import MPTTModelAdmin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price', 'stock_quantity']
    list_filter = ['type', 'category']
    search_fields = ['name', 'isbn', 'ean']


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_display = ['name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']


admin.site.register(SelectedProduct)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Autor)
