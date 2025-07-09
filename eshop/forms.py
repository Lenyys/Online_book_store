from django import forms

from eshop.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
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
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Jmeno autora'}),
            'autor': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }



