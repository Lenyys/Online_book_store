from django.test import TestCase

from eshop.forms import BookForm, AuthorForm, AddOrCreateAuthorForm
from eshop.models import Autor, Category


class BookTestForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.autor = Autor.objects.create(name='autor_f', lastname='autor_l')
        cls.category = Category.objects.create(name='komiksy')

    def test_book_form_is_valid(self):
        book_form = BookForm(data={
            'name':'kniha',
            'type':'book',
            'autor': [self.autor.pk],
            'price': 100,
            'description': 'Popis',
            'stock_quantity': 5,
            'category': [self.category.id],
            'isbn': '978-3-16-148410-0',
            'ean': 1234567891012,
        })
        self.assertTrue(book_form.is_valid())

    def test_book_form_price(self):
        book_form = BookForm(data={
            'name': 'kniha',
            'type': 'book',
            'autor': [self.autor.pk],
            'price': -2,
            'description': 'Popis',
            'stock_quantity': 5,
            'category': [self.category.id],
            'isbn': '978-3-16-148410-0',
            'ean': 1234567891012,
        })
        self.assertFalse(book_form.is_valid())

    def test_book_form_isbn(self):
        book_form = BookForm(data={
            'name': 'kniha',
            'type': 'book',
            'autor': [self.autor.pk],
            'price': -2,
            'description': 'Popis',
            'stock_quantity': 5,
            'category': [self.category.id],
            'isbn': '978-3-16-1484',
            'ean': 1234567891012,
        })
        self.assertFalse(book_form.is_valid())

class AuthorTestForm(TestCase):
    def test_author_form_valid(self):
        author_form = AuthorForm(
            data={
                'name': 'Autor',
                'lastname': 'Autor-p',
            }
        )
        self.assertTrue(author_form.is_valid())

    def test_author_form_invalid(self):
        author_form = AuthorForm(
            data={
                'name': 'Autor',
                'lastname': '',
            }
        )
        self.assertFalse(author_form.is_valid())

class TestAddOrCreateAuthorForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existing_author = Autor.objects.create(name='existing', lastname='autor')

    def test_add_existing_autor_to_book_valid(self):
        add_or_create_author_book = AddOrCreateAuthorForm(
           data={
               'existing_author': self.existing_author.pk,
               'new_author_name': '',
               'new_author_lastname':'',
           })
        self.assertTrue(add_or_create_author_book.is_valid())

    def test_add_no_existing_autor_to_book_valid(self):
        add_or_create_author_book = AddOrCreateAuthorForm(
           data={
               'existing_author': '',
               'new_author_name': 'new',
               'new_author_lastname':'autor',
           })
        self.assertTrue(add_or_create_author_book.is_valid())
