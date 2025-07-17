from django import forms
from django.core.exceptions import ValidationError

from eshop.models import Book, Category, Image, Autor


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


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']

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

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('existing_author') and \
            not cleaned_data.get('new_author_name') and \
                not cleaned_data.get('new_author_lastname'):
            raise forms.ValidationError('Vyber autora nebo zadej nového')
        return cleaned_data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'



