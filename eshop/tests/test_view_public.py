from django.test import TestCase
from django.urls import reverse

from eshop.models import Category, Book, Autor


class BookListViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Sci-Fi')
        book = Book.objects.create(name='Book A', price=100, description="Popis")
        book.category.set([self.category])
        Book.objects.create(name='Book B', price=200)

    def test_book_list_view_status_code(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book A')
        self.assertContains(response, 'Book B')

    def test_book_list_filtering_by_category(self):
        response = self.client.get(reverse('book_list') + f'?category={self.category.id}')
        self.assertContains(response, 'Book A')
        self.assertNotContains(response, 'Book B')


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Sci-Fi')
        self.autor = Autor.objects.create(name='Test', lastname='Autor')
        self.book = Book.objects.create(name='Book A', price=100, description="popis")
        self.book.category.set([self.category])
        self.book.autor.set([self.autor])

    def test_detail_view_status_code(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Book A')
        self.assertContains(response,  100)
        self.assertContains(response, 'popis')
        self.assertContains(response, 'Test Autor')
        self.assertContains(response, 'Přidat do košíku')
        self.assertNotContains(response, 'Produkt vyprodán')


