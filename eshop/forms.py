from django import forms
from django.core.exceptions import ValidationError

from eshop.models import Book, Category, Image


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','autor','price', 'description', 'stock_quantity',
            'category', 'isbn', 'ean']
        labels = {
            'name': 'Název knihy',
            'autor': 'Autor',
            'price': 'Cena',
            'description': 'Popis',
            'stock_quantity': 'Dostupné množství',
            'category': 'Kategorie',
            'isbn': 'ISBN',
            'ean': 'EAN',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nazev knihy'
            }),
            'autor': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
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
        if price is not None and price <= 0:
            raise forms.ValidationError("Cena musí být větší než 0 Kč.")
        return price

    def clean(self):
        cleaned_data = super().clean()
        isbn = cleaned_data.get('isbn')
        ean = cleaned_data.get('ean')

        if not isbn and not ean:
            raise forms.ValidationError("Musíte zadat alespoň ISBN nebo EAN.")

        if isbn and len(isbn.replace('-', '').strip()) < 10:
            self.add_error('isbn', "ISBN vypadá příliš krátce – zkontrolujte formát.")

        return cleaned_data

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']





class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



