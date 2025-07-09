
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category(name={self.name})"

class Autor(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    lastname = models.CharField(max_length=150, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    autor = models.ManyToManyField(Autor, related_name='products')
    isbn = models.CharField(max_length=20, null=True, blank=True)
    ean = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    stock_quantity = models.PositiveIntegerField(null=False, blank=True, default=0)
    category = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='products_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='products_updated')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.price}Kč)"

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price}, description={self.description})"


class Image(models.Model):
    image = models.ImageField(upload_to='images/', default=None, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    description = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['product']

    def __str__(self):
        return f"Image: {self.image}"

    def __repr__(self):
        return f"Image(image={self.image})"


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_temporary = models.BooleanField(null=False, default=True)

    def __str__(self):
        pass

    def __repr__(self):
        pass


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True, default=0)
    delivery_address = models.TextField(null=False, blank=False)

    def __str__(self):
        pass

    def __repr__(self):
        pass


class SelectedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=False)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True, default=0)
    quantity = models.PositiveIntegerField(null=False, blank=True, default=0)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_products')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        pass
    def __repr__(self):
        pass

