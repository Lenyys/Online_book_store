from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from eshop.models import Book, Category, Autor, Image


class StaffBookViewsTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        # všechny permissions
        content_type = ContentType.objects.get_for_model(Book)
        permissions = Permission.objects.filter(content_type=content_type)
        self.staff_user.user_permissions.set(permissions)
        # # jen konkrétní permissions
        # permission = Permission.objects.get(codename='add_book')
        # self.staff_user.user_permissions.add(permission)
        self.book = Book.objects.create(name='Test Book', price=150, description='testík')

    def test_staff_book_list_requires_login(self):
        response = self.client.get(reverse('staff_book_list'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(reverse('staff_book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Přidat knihu')
        self.assertContains(response, 'Seznam Knih')

    def test_book_create_view_post(self):
        self.client.login(username='staff', password='pass1234test')
        self.category = Category.objects.create(name='Sci-Fi')
        self.autor = Autor.objects.create(name='Test', lastname='Autor')
        response = self.client.post(reverse('book_create'), {
            'name': 'New Book',
            'price': 123,
            'type': 'book',
            'description': 'Popis new book',
            'isbn': '978-3-16-148410-0',
            'ean': 1234567891012,
            'autor': [self.autor.pk],
            'category': [self.category.pk]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(name='New Book').exists())
        self.assertRedirects(response, reverse('staff_book_list'))

    # @skip
    def test_book_create_view_post_blank_m2m(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.post(reverse('book_create'), {
            'name': 'New Book',
            'price': 123,
            'type': 'book',
            'description': 'Popis new book',
            'isbn': '978-3-16-148410-0',
            'ean': 1234567890101
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(name='New Book').exists())
        self.assertRedirects(response, reverse('staff_book_list'))

    def test_book_create_view_get(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(reverse('book_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        back_url = reverse('staff_book_list')
        self.assertContains(response, 'Zpět na seznam knih')
        self.assertContains(response, f'href="{back_url}"')


class StaffBookDetailViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        book_ct = ContentType.objects.get_for_model(Book)
        autor_ct = ContentType.objects.get_for_model(Autor)
        image_ct = ContentType.objects.get_for_model(Image)
        book_perms = Permission.objects.filter(content_type=book_ct)
        autor_perms = Permission.objects.filter(content_type=autor_ct)
        image_perms = Permission.objects.filter(content_type=image_ct)
        permissions = book_perms | autor_perms | image_perms
        self.staff_user.user_permissions.set(permissions)
        self.book = Book.objects.create(name='Test Book', price=150, description='testík')

    def test_staff_book_detail(self):
        self.client.login(username='staff', password='pass1234test')
        self.category = Category.objects.create(name='Sci-Fi')
        self.autor = Autor.objects.create(name='Test', lastname='Autor')
        self.book.category.set([self.category])
        self.book.autor.set([self.autor])
        response = self.client.get(reverse('staff_book_detail', kwargs={'pk': self.book.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upravit')
        self.assertContains(response, 'Smazat')
        self.assertContains(response, 'Zpět')
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'testík')
        self.assertContains(response, 150)
        self.assertContains(response, 'Test Autor')
        self.assertContains(response, 'Sci-Fi')
        self.assertContains(response, '+ Autor')
        self.assertContains(response, 'Odebrat')
        self.assertContains(response, '+ Obrázek')

    def test_add_or_create_autor_view_get(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(reverse('add_or_create_author', kwargs={'pk': self.book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        back_url = reverse('staff_book_detail', kwargs={'pk': self.book.id})
        self.assertContains(response, 'Zpět')
        self.assertContains(response, f'href="{back_url}"')

    def test_add_or_create_autor_view_post(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.post(
            reverse('add_or_create_author', kwargs={'pk': self.book.id}),
            {
                'new_author_name': 'Jan',
                'new_author_lastname': 'Novák',
                'new_author_birthdate': '1980-01-01'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('staff_book_detail', kwargs={'pk': self.book.id}))
        self.assertEqual(self.book.autor.count(), 1)
        autor = self.book.autor.first()
        self.assertEqual(autor.name, 'Jan')
        self.assertEqual(autor.lastname, 'Novák')
        self.assertTrue(Autor.objects.filter(name='Jan', lastname="Novák").exists())

    def test_add_or_create_view_existing_author_post(self):
        self.client.login(username='staff', password='pass1234test')
        author = Autor.objects.create(name='Jan', lastname='Novák')
        response = self.client.post(
            reverse('add_or_create_author', kwargs={'pk': self.book.id}),
            {
                'existing_author': author.id
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(author in self.book.autor.all())
        self.assertRedirects(response, reverse('staff_book_detail', kwargs={'pk': self.book.id}))

    def test_remove_autor_from_book_view_get(self):
        self.client.login(username='staff', password='pass1234test')
        author = Autor.objects.create(name='Jan', lastname='Novák')
        self.book.autor.set([author])
        next_url = reverse('staff_book_detail', kwargs={'pk': self.book.id})
        response = self.client.get(reverse('remove_author', kwargs={
            'book_id': self.book.id,
            'author_id': author.id,
        }) + f'?next={next_url}')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{next_url}"')
        self.assertContains(response, 'Zpět na detail knihy')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'type="hidden"')
        self.assertContains(response, '<form')
        self.assertContains(response, 'Novák')

    def test_remove_autor_from_book_view_post(self):
        self.client.login(username='staff', password='pass1234test')
        author = Autor.objects.create(name='Jan', lastname='Novák')
        self.book.autor.set([author])
        next_url = reverse('staff_book_detail', kwargs={'pk': self.book.id})
        response = self.client.post(
            reverse('remove_author', kwargs={
                'book_id': self.book.id,
                'author_id': author.id,
            }) + f'?next={next_url}', {})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, next_url)
        self.assertFalse(self.book.autor.filter(id=author.id).exists())
        self.assertTrue(Autor.objects.filter(name='Jan', lastname='Novák').exists())


class BookUpdateViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        book_ct = ContentType.objects.get_for_model(Book)
        image_ct = ContentType.objects.get_for_model((Image))
        book_perm = Permission.objects.filter(content_type=book_ct)
        image_perm = Permission.objects.filter(content_type=image_ct)
        permissions = book_perm | image_perm
        self.staff_user.user_permissions.set(permissions)
        self.book = Book.objects.create(name='Test Book', price=150, description='testík')

    def test_book_update_get(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_book_detail', kwargs={'pk': self.book.id})
        response = self.client.get(
            reverse('book_update', kwargs={'pk': self.book.id}) + f'?next={next_url}')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{next_url}"')
        self.assertContains(response, 'Zpět')
        self.assertContains(response, '<form')
        self.assertContains(response, 'Editace knihy')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'type="hidden"')

    def test_book_update_post(self):
        self.client.login(username='staff', password='pass1234test')
        author = Autor.objects.create(name='Jan', lastname='Novák')
        self.book.autor.set([author])
        category = Category.objects.create(name='Test')
        self.book.category.set([category])
        next_url = reverse('staff_book_list')
        response = self.client.post(
            reverse('book_update', kwargs={
                'pk': self.book.id}) + f'?next={next_url}', {
                'name': 'New Name',
                'type': 'book',
                'autor': [author.id],
                'category': [category.id],
                'price': self.book.price,
                'description': self.book.description,
                'ean': 1234567891011
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, next_url)
        self.assertTrue(Book.objects.filter(name='New Name').exists())
        self.assertFalse(Book.objects.filter(name='Test Book').exists())


class BookDeleteViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        book_ct = ContentType.objects.get_for_model(Book)
        permissions = Permission.objects.filter(content_type=book_ct)
        self.staff_user.user_permissions.set(permissions)
        self.book = Book.objects.create(name='Test Book', price=150, description='testík')

    def test_book_delete_get(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_book_detail', kwargs={'pk': self.book.id})
        response = self.client.get(
            reverse('book_delete', kwargs={'pk': self.book.id}) + f'?next={next_url}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="{next_url}"')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'type="hidden"')
        self.assertContains(response, 'Opravdu chcete odstranit knihu:')

    def test_book_delete_post(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_book_list')
        response = self.client.post(
            reverse('book_delete', kwargs={
                'pk': self.book.id}) + f'?next={next_url}', {}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, next_url)
        self.assertFalse(Book.objects.filter(name='Test Book').exists())


class ImageTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        book_ct = ContentType.objects.get_for_model(Book)
        image_ct = ContentType.objects.get_for_model(Image)
        book_perms = Permission.objects.filter(content_type=book_ct)
        image_perms = Permission.objects.filter(content_type=image_ct)
        permissions = book_perms | image_perms
        self.staff_user.user_permissions.set(permissions)
        self.book = Book.objects.create(name='Test Book', price=150, description='testík')

    def test_add_image_view_get(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(
            reverse('add_image', kwargs={'pk': self.book.id})
        )
        back_url = reverse('staff_book_detail', kwargs={'pk': self.book.id})
        self.assertContains(response, 'Zpět')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, 'Přidání obrázku ke knize:')
        self.assertContains(response, f'href="{back_url}"')


class StaffAuthorListViewTest(TestCase):

    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        author_ct = ContentType.objects.get_for_model(Autor)
        permissions = Permission.objects.filter(content_type=author_ct)
        self.staff_user.user_permissions.set(permissions)
        self.author = Autor.objects.create(name='Jan', lastname='Novák')

    def test_staff_author_list_get(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(
            reverse('staff_author_list')
        )
        back_url = reverse('staff_author_list')
        back_url_create = reverse('author_create')
        back_url_delete = reverse('author_delete', kwargs={'pk': self.author.id}) + f'?next={back_url}'
        back_url_update = reverse('author_update', kwargs={'pk': self.author.id}) + f'?next={back_url}'
        back_url_detail = reverse('staff_author_detail', kwargs={'pk': self.author.id}) + f'?next={back_url}'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Seznam Autorů')
        self.assertContains(response, f'href="{back_url}"')
        self.assertContains(response, f'href="{back_url_create}"')
        self.assertContains(response, f'href="{back_url_delete}"')
        self.assertContains(response, f'href="{back_url_update}"')
        self.assertContains(response, f'href="{back_url_detail}"')
        self.assertContains(response, 'Novák')


class AuthorCreateViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        author_ct = ContentType.objects.get_for_model(Autor)
        permissions = Permission.objects.filter(content_type=author_ct)
        self.staff_user.user_permissions.set(permissions)

    def test_author_create_get(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(
            reverse('author_create')
        )
        back_url = reverse('staff_author_list')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, f'href="{back_url}"')
        self.assertContains(response, 'Přidání autora:')

    def test_author_create_post(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.post(
            reverse('author_create'), {
                'name': 'Jan',
                'lastname': 'Novák'
            }
        )
        back_url = reverse('staff_author_list')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, back_url)
        self.assertTrue(Autor.objects.filter(name='Jan', lastname='Novák').exists())


class StaffAuthorDetailViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        author_ct = ContentType.objects.get_for_model(Autor)
        permissions = Permission.objects.filter(content_type=author_ct)
        self.staff_user.user_permissions.set(permissions)
        self.author = Autor.objects.create(name='Jan', lastname='Novák')

    def test_author_detail_get(self):
        self.client.login(username='staff', password='pass1234test')
        response = self.client.get(
            reverse('staff_author_detail', kwargs={'pk': self.author.id})
        )
        back_url = reverse('staff_author_list')
        next_url = reverse('staff_author_detail', kwargs={'pk': self.author.id})
        update_url = reverse('author_update', kwargs={'pk': self.author.id}) + f'?next={next_url}'
        delete_url = reverse('author_delete', kwargs={'pk': self.author.id}) + f'?next={next_url}'

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail autora')
        self.assertContains(response, 'Novák')
        self.assertContains(response, f'href="{back_url}"')
        self.assertContains(response, f'href="{update_url}"')
        self.assertContains(response, f'href="{delete_url}"')


class AuthorUpdateViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        author_ct = ContentType.objects.get_for_model(Autor)
        permissions = Permission.objects.filter(content_type=author_ct)
        self.staff_user.user_permissions.set(permissions)
        self.author = Autor.objects.create(name='Jan', lastname='Novák')

    def test_author_update_get(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_author_list')
        response = self.client.get(
            reverse('author_update', kwargs={'pk': self.author.id}) + f'?next={next_url}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upravení autora')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, f'href="{next_url}"')
        self.assertContains(response, f'type="hidden"')

    def test_author_update_post(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_author_list')
        response = self.client.post(
            reverse('author_update', kwargs={
                'pk': self.author.id}) + f'?next={next_url}', {
                'name': 'Josef',
                'lastname': self.author.lastname
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, next_url)
        self.assertTrue(Autor.objects.filter(name='Josef').exists())
        self.assertFalse(Autor.objects.filter(name='Jan').exists())


class AuthorDeleteViewTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username='staff', password='pass1234test', is_staff=True)
        author_ct = ContentType.objects.get_for_model(Autor)
        permissions = Permission.objects.filter(content_type=author_ct)
        self.staff_user.user_permissions.set(permissions)
        self.author = Autor.objects.create(name='Jan', lastname='Novák')

    def test_author_delete_get(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_author_list')
        response = self.client.get(
            reverse('author_delete', kwargs={'pk': self.author.id}) + f'?next={next_url}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Opravdu chcete odstranit autora')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, f'href="{next_url}"')
        self.assertContains(response, f'type="hidden"')

    def test_author_delete_post(self):
        self.client.login(username='staff', password='pass1234test')
        next_url = reverse('staff_author_list')
        response = self.client.post(
            reverse('author_delete', kwargs={
                'pk': self.author.id}) + f'?next={next_url}', {}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, next_url)
        self.assertFalse(Autor.objects.filter(name='Jan').exists())
