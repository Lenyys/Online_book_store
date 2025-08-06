from django.test import TestCase

from django.contrib.auth.models import User

from eshop.models import Book, Autor, Category


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            name='Book',
            type='book',
            isbn='978-3-16-148410-0',
            ean=1234567891012,
            description='Popis',
            price=100,
            stock_quantity=10,
        )
        author = Autor.objects.create(name='autor', lastname='prijmeni')
        cls.book.autor.add(author)

        category = Category.objects.create(name='kategorie')
        category_2 = Category.objects.create(name='druha')
        cls.book.category.add(category, category_2)

    def test_book_exists(self):
        book = Book.objects.get(name='Book')
        self.assertIsNotNone(book)

    def test_name(self):
        self.assertEqual(self.book.name, 'Book')

    def test_book_categories_count(self):
        num_of_categories = self.book.category.count()
        self.assertEqual(num_of_categories, 2)
