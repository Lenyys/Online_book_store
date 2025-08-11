

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from eshop.models import Book, Cart, SelectedProduct


class AddProductToCartTest(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name="testbook1", price=100, stock_quantity=4)
        self.book_2 = Book.objects.create(name="testbook2", price=200, stock_quantity=0)
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_add_to_cart_no_user(self):
        response = self.client.post(reverse('add_to_cart',
                                            kwargs={'pk': self.book_1.id}), {})
        session_key = self.client.session.session_key
        cart = Cart.objects.get(session_key=session_key)
        cart_item = SelectedProduct.objects.get(cart=cart, product=self.book_1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_detail'))
        self.assertEqual(cart_item.product.name,"testbook1")
        self.assertEqual(cart_item.quantity,1)

    def test_no_stock_quantity_no_adding_button(self):
        response = self.client.get(reverse('book_detail', kwargs={'pk':self.book_2.id}))

        self.assertContains(response, 'Produkt je vyprodán')
        self.assertNotContains(response, 'Přidat do košíku')

    def test_add_to_cart_user_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_to_cart',
                                            kwargs={'pk': self.book_1.id}), {})
        cart = Cart.objects.get(user=self.user)
        cart_item = SelectedProduct(cart=cart, product=self.book_1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_detail'))
        self.assertEqual(cart_item.product.name, "testbook1")
        self.assertEqual(cart_item.quantity, 1)

    def test_add_same_item_twice(self):
        self.client.post(reverse('add_to_cart', kwargs={'pk': self.book_1.id}),{})
        self.client.post(reverse('add_to_cart', kwargs={'pk': self.book_1.id}), {})

        session_key = self.client.session.session_key
        cart = Cart.objects.get(session_key=session_key)
        cart_item = SelectedProduct.objects.get(cart=cart, product=self.book_1)

        self.assertEqual(cart_item.quantity, 2)


class CartDetailViewTest(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name="testbook1", price=100, stock_quantity=4)
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = SelectedProduct.objects.create(cart=self.cart, product=self.book_1)

    def test_cart_detail_user_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('cart_detail'))
        continue_url = reverse('book_list')
        remove_url = reverse('remove_from_cart', kwargs={'pk':self.cart_item.id})
        update_cart_url = reverse('update_cart')


        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testbook1")
        self.assertContains(response, 100)
        self.assertContains(response, '<input type="number"')
        self.assertContains(response, 'type="submit"')
        self.assertContains(response, "<form")
        self.assertContains(response, f'action="{update_cart_url}"')
        self.assertContains(response, f'href="{continue_url}"')
        self.assertContains(response, f'href="{remove_url}"')

    def test_remove_item_from_cart(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('remove_from_cart', kwargs={'pk':self.cart_item.id}), {})

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response, reverse('cart_detail'))
        self.assertFalse(SelectedProduct.objects.filter(id=self.cart_item.id).exists())
        self.assertFalse(self.cart.selected_products.filter(id=self.cart_item.id).exists())


    def test_change_quantity(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('update_cart'), {
            f'quantity-{self.cart_item.id}':'3',
        })
        refreshed_item = SelectedProduct.objects.get(id=self.cart_item.id)
        self.assertEqual(response.status_code,302)
        self.assertEqual(refreshed_item.quantity,3)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity,3)