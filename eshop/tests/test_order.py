
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from eshop.models import Book, Cart, SelectedProduct, Order


class CreateOrderWithFormViewTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            name='test',
            price='123',
            stock_quantity=4
        )

    def test_order_no_user(self):
        session = self.client.session
        session.save()
        session_key = session.session_key
        cart = Cart.objects.create(session_key=session_key)
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            cart=cart
        )
        response = self.client.get(reverse('create_order'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'objednávka')
        self.assertContains(response, 'Odeslat objednávku')
        self.assertContains(response, 'type="submit"')

    def test_order_no_user_post(self):
        session = self.client.session
        session.save()
        session_key = session.session_key
        cart = Cart.objects.create(session_key=session_key)
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            cart=cart
        )
        response = self.client.post(reverse('create_order'),{
            'first_name':'Jan',
            'last_name':'Novák',
            'email':'jan@test.cz',
            'phone':'697123456',
            'delivery_address':'Kolbenova 9',
            'city': 'Praha',
            'postal_code': '11000'

        })

        order = Order.objects.get(first_name='Jan', last_name='Novák')

        self.assertEqual(response.status_code, 302)
        next_url = reverse('order_detail', kwargs={'pk':order.id})
        self.assertRedirects(response, next_url)
        self.assertTrue(Order.objects.filter(first_name='Jan', last_name='Novák').exists())

    def test_order_user_authenticated(self):
        user = User.objects.create_user(username='testuser', password='heslo1234')
        self.client.login(username='testuser', password='heslo1234')
        cart = Cart.objects.create(user=user)
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            cart=cart
        )
        response = self.client.get(reverse('create_order'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'objednávka')
        self.assertContains(response, 'Odeslat objednávku')
        self.assertContains(response, 'type="submit"')

    def test_order_user_authenticated_post(self):
        user = User.objects.create_user(username='testuser', password='heslo1234')
        self.client.login(username='testuser', password='heslo1234')

        cart = Cart.objects.create(user=user)
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            cart=cart
        )
        response = self.client.post(reverse('create_order'), {
            'first_name': 'Jan',
            'last_name': 'Novák',
            'email': 'jan@test.cz',
            'phone': '697123456',
            'delivery_address': 'Kolbenova 9',
            'city': 'Praha',
            'postal_code': '11000'

        })

        order = Order.objects.get(user=user)

        self.assertEqual(response.status_code, 302)
        next_url = reverse('order_detail', kwargs={'pk': order.id})
        self.assertRedirects(response, next_url)
        self.assertTrue(Order.objects.filter(first_name='Jan', last_name='Novák').exists())

    def test_order_detail(self):
        user = User.objects.create_user(username='testuser', password='heslo1234')
        self.client.login(username='testuser', password='heslo1234')
        order = Order.objects.create(
            user=user,
            total_price=self.book.price,
            delivery_address= 'Kolbenova 9 Praha',
            first_name='Jan',
            last_name='Novák',
            email = 'jan@test.cz',
            phone = '697123456',
            postal_code='11001'
        )
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            order=order
        )
        response = self.client.get(reverse('order_detail', kwargs={'pk':order.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shrnutí objednávky')
        self.assertContains(response, self.book.name)
        self.assertContains(response, 'Závazně odeslat objednávku')

    def test_order_detail_post_order_sent(self):
        user = User.objects.create_user(username='testuser', password='heslo1234')
        self.client.login(username='testuser', password='heslo1234')
        order = Order.objects.create(
            user=user,
            total_price=self.book.price,
            delivery_address='Kolbenova 9 Praha',
            first_name='Jan',
            last_name='Novák',
            email='jan@test.cz',
            phone='697123456',
            postal_code='11001'
        )
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            order=order
        )
        response = self.client.post(reverse('order_sent', kwargs={'pk':order.id}),{})

        self.assertEqual(response.status_code, 302)
        next_url = reverse('order_confirmation', kwargs={'pk':order.id})
        self.assertRedirects(response, next_url)


    def test_order_detail_order_confirm(self):
        user = User.objects.create_user(username='testuser', password='heslo1234')
        self.client.login(username='testuser', password='heslo1234')
        order = Order.objects.create(
            user=user,
            total_price=self.book.price,
            delivery_address='Kolbenova 9 Praha',
            first_name='Jan',
            last_name='Novák',
            email='jan@test.cz',
            phone='697123456',
            postal_code='11001'
        )
        SelectedProduct.objects.create(
            product=self.book,
            quantity=1,
            order=order
        )

        response = self.client.get(reverse('order_confirmation', kwargs={'pk':order.id}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'Děkujeme za objednávku!')
        self.assertContains(response, order.id)
        self.assertContains(response, self.book.price)

