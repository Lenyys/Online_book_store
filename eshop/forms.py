import datetime
import re

from django import forms
from django.core.exceptions import ValidationError

from eshop.models import Book, Category, Image, Autor, Order


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'type', 'autor', 'price', 'discount', 'description', 'stock_quantity',
                  'category', 'isbn', 'ean']
        labels = {
            'name': 'Název knihy',
            'type': 'Typ knihy',
            'autor': 'Autor',
            'price': 'Cena',
            'discount': 'Sleva v %',
            'description': 'Popis',
            'stock_quantity': 'Dostupné množství',
            'category': 'Kategorie',
            'isbn': 'ISBN',
            'ean': 'EAN',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazev knihy'
            }),
            'autor': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Popis knihy',
                'rows': 4
            }),
            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Počet kusů skladem'
            }),
            'category': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Např. 978-3-16-148410-0'
            }),
            'ean': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'EAN kód'
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError
        name = name.strip()
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price or price <= 0:
            raise forms.ValidationError("Cena musí být větší než 0 Kč.")
        return price

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if not discount:
            return discount
        if discount < 0 or discount > 100:
            raise forms.ValidationError("Sleva je v rozsahu 0-100")
        return discount

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn:
            return isbn
        isbn = isbn.replace('-', '').strip()
        if len(isbn) != 13:
            raise forms.ValidationError("ISBN musí obsahovat 13 číslic")
        if not (isbn.startswith('978') or isbn.startswith('979')):
            raise forms.ValidationError("isbn musí začínat na 978 nebo 979")

        def checksum(isbn_str):
            total = 0
            for i, digit in enumerate(isbn_str[:12]):
                num = int(digit)
                total += num if i % 2 == 0 else num * 3
            div_remainder = total % 10
            if div_remainder == 0:
                check_num = 0
            else:
                check_num = 10 - div_remainder
            return check_num == int(isbn_str[-1])

        if not checksum(isbn):
            raise forms.ValidationError("Kontrolní číslo neodpovídá zadanému isbn")
        return isbn

    def clean_ean(self):
        ean = self.cleaned_data.get('ean')
        if not ean:
            return ean
        if len(str(ean)) != 13:
            raise forms.ValidationError("ean musí obsahovat 13 čísel")
        return ean


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']

        labels = {
            'image': 'obrázek',
            'description': 'Popis k obrázku'
        }


class AddOrCreateAuthorForm(forms.Form):
    existing_author = forms.ModelChoiceField(
        queryset=Autor.objects.all(),
        required=False,
        label='Autor'
    )
    new_author_name = forms.CharField(
        required=False,
        label='Jméno nového autora'
    )
    new_author_lastname = forms.CharField(
        required=False,
        label='Příjmení nového autora'
    )
    new_author_birthdate = forms.DateField(
        required=False,
        label='datum narození nového autora'
    )

    def clean_new_author_name(self):
        name = self.cleaned_data.get('new_author_name')
        if not name:
            return name
        if not re.match(r'^[A-Za-zÁ-Žá-ž\s\-]+$', name):
            raise forms.ValidationError("Jméno může obsahovat pouze písmena, mezery a pomlčky")
        name = name.title()
        return name

    def clean_new_author_lastname(self):
        lastname = self.cleaned_data.get('new_author_lastname')
        if not lastname:
            return lastname
        if not re.match(r'^[A-Za-zÁ-Žá-ž\s\-]+$', lastname):
            raise forms.ValidationError("Jméno může obsahovat pouze písmena, mezery a pomlčky")
        lastname = lastname.title()
        return lastname

    def clean_new_author_birthdate(self):
        dob = self.cleaned_data.get('new_author_birthdate')
        if dob is None:
            return dob
        try:
            if dob > datetime.date.today():
                raise forms.ValidationError("Datum narození nemůže být v budoucnosti")
        except TypeError:
            raise forms.ValidationError("Neplatné datum")
        return dob

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('existing_author') and \
                not (cleaned_data.get('new_author_name') and
                     cleaned_data.get('new_author_lastname')):
            raise forms.ValidationError('Vyber autora nebo zadej nového')
        return cleaned_data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'
        labels = {
            'name': 'Jméno',
            'lastname': 'Příjmení',
            'date_of_birth': 'Datum narození'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Karel'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Novák'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError("Jméno je povinné")
        if not re.match(r'^[A-Za-zÁ-Žá-ž\s\-]+$', name):
            raise forms.ValidationError("Jméno může obsahovat pouze písmena, mezery a pomlčky")
        name = name.title()
        return name

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname:
            raise forms.ValidationError("Příjmení je povinné")
        if not re.match(r'^[A-Za-zÁ-Žá-ž\s\-]+$', lastname):
            raise forms.ValidationError("Jméno může obsahovat pouze písmena, mezery a pomlčky")
        lastname = lastname.title()
        return lastname

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob is None:
            return dob
        try:
            if dob > datetime.date.today():
                raise forms.ValidationError("Datum narození nemůže být v budoucnosti")
        except TypeError:
            raise forms.ValidationError("Neplatné datum")
        return dob

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('name') and cleaned_data.get('lastname')):
            raise forms.ValidationError('Autor musí mít jméno a příjmení')
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'delivery_address', 'postal_code', 'note']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '607123456'}),
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', }),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', }),
            'note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', }),
        }

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if not re.match(r'^[A-Za-zÁ-Žá-ž\s\-]+$', name):
            raise forms.ValidationError("Jméno může obsahovat pouze písmena, mezery a pomlčky")
        name = name.title()
        return name

    def clean_last_name(self):
        lastname = self.cleaned_data.get('last_name')
        if not re.match(r'^[A-Za-zÁ-Žá-ž\s\-]+$', lastname):
            raise forms.ValidationError("Jméno může obsahovat pouze písmena, mezery a pomlčky")
        lastname = lastname.title()
        return lastname

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        phone_clean = phone.replace(" ", "")
        if not re.match(r'^(\+420)?[0-9]{9}$', phone_clean):
            raise forms.ValidationError("neplatné telefoní číslo")
        return phone_clean

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if not re.match(r'^\d{3}\s?\d{2}$', postal_code):
            raise forms.ValidationError("psč obsahuje 5 číslic")

        psc = postal_code.replace(" ", "")
        return psc
