from PIL import Image as PILImage, UnidentifiedImageError
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Category(name={self.name})"


class Autor(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    lastname = models.CharField(max_length=150, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.lastname}"

    def __repr__(self):
        return f"Autor(name={self.name}, lastname={self.lastname})"


class Book(models.Model):
    TYPE_CHOICES = [
        ('book', 'Tištěná kniha'),
        ('ebook', 'E-kniha'),
        ('audiobook', 'Audiokniha'),
    ]
    name = models.CharField(max_length=150, null=False, blank=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='book')  # <-- TADY
    autor = models.ManyToManyField(Autor, blank=True, related_name='books')
    isbn = models.CharField(max_length=20, null=True, blank=True)
    ean = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    stock_quantity = models.PositiveIntegerField(null=False, blank=True, default=1)
    category = models.ManyToManyField(Category, blank=True, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='products_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='products_updated')
    favorite_book = models.ManyToManyField(User, blank=True, related_name='favorite_books')
    discount = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, default=0)

    class Meta:
        ordering = ['name']

    def get_discount_price(self):
        if self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price

    def __str__(self):
        return f"{self.name} ({self.price}Kč)"

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price}, description={self.description})"


class Image(models.Model):
    image = models.ImageField(upload_to='eshop/images/', default=None, null=False, blank=False)
    product = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    description = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ['product']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img_path = self.image.path
        try:
            img = PILImage.open(img_path)
            max_size = (800, 800)

            if img.height > 800 or img.width > 800:
                img.thumbnail(max_size)
                img.save(img_path, quality=85, optimize=True)

        except UnidentifiedImageError:
            # Tento typ chyby nastane, pokud soubor není obrázek
            print(f"Soubor {img_path} není platný obrázek.")
        except FileNotFoundError:
            print(f"Soubor {img_path} nebyl nalezen.")
        except Exception as e:
            # Pro všechny ostatní chyby (např. při ukládání)
            print(f"Chyba při zpracování obrázku: {e}")

    def __str__(self):
        return f"Image: {self.image}"

    def __repr__(self):
        return f"Image(image={self.image})"


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_temporary = models.BooleanField(null=False, default=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"košík uživatele {self.user}"
        return f"košík na session {self.session_key}"

    def __repr__(self):
        if self.user:
            return f"Cart(user={self.user}"
        return f"Cart(session_key={self.session_key}"

    def get_total_cart_price(self):
        total_price = 0
        for item in self.selected_products.all():
            total_price += (item.product.price * item.quantity)
        return total_price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True, default=0)
    delivery_address = models.TextField(null=False, blank=False)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(default='')
    phone = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=10, default="")
    note = models.TextField(blank=True)

    def __str__(self):
        return f"objednávka #{self.id} - {self.first_name} {self.last_name}"

    def __repr__(self):
        return (f"Order(first_name={self.first_name},"
                f"lastname={self.last_name}, delivery_address={self.delivery_address}")


class SelectedProduct(models.Model):
    product = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=False)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True, default=0)
    quantity = models.PositiveIntegerField(null=False, blank=True, default=1)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_products')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='selected_products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} ({self.quantity})"

    def __repr__(self):
        return f"SelectedProduct(product={self.product})"
