from django.contrib import admin

from eshop.models import Category, Book, SelectedProduct, Image, Order, Cart, Autor

# Register your models here.

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(SelectedProduct)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Autor)
