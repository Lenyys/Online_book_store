from django.contrib import admin

from eshop.models import Category, Product, SelectedProduct, Image, Order, Cart

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(SelectedProduct)
admin.site.register(Image)
admin.site.register(Cart)
admin.site.register(Order)
