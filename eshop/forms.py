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


class OrderForm(forms.Form):
    delivery_addres = forms
    first_name = forms.CharField(label='Jméno', max_length=50)
    last_name = forms.CharField(label='Příjmení', max_length=50)
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefon', max_length=20, required=False)
    delivery_address = forms.CharField(
        label='Dodací adresa',
        widget=forms.Textarea(attrs={'rows': 3}),
    )
    city = forms.CharField(label='Město', max_length=100)
    postal_code = forms.CharField(label='PSČ', max_length=10)
    note = forms.CharField(
        label='Poznámka k objednávce',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False
    )

    # accept_terms = forms.BooleanField(label='Souhlasím s obchodními podmínkami')
    #
    # DELIVERY_CHOICES = [
    #     ('ppl', 'PPL kurýr'),
    #     ('zasilkovna', 'Zásilkovna'),
    #     ('osobne', 'Osobní odběr'),
    # ]
    # delivery_method = forms.ChoiceField(
    #     choices=DELIVERY_CHOICES,
    #     label='Způsob doručení'
    # )
    #
    # PAYMENT_CHOICES = [
    #     ('dobirka', 'Dobírka'),
    #     ('prevod', 'Bankovní převod'),
    #     ('online', 'Online platba kartou'),
    # ]
    # payment_method = forms.ChoiceField(
    #     choices=PAYMENT_CHOICES,
    #     label='Způsob platby'
    # )