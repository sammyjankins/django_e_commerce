from django.test import TestCase, Client
from django.urls import reverse

from coupons.forms import CouponApplyForm
from shop.models import Product, Category


class CartAddViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', slug='test-product',
                                              price=10.00, category=self.category)

    def test_cart_add_view(self):
        client = Client()
        url = reverse('cart:cart_add', args=[self.product.id])

        response = client.post(url, {'quantity': 2, 'override': False})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))

        cart = response.wsgi_request.session['cart']
        self.assertTrue(str(self.product.id) in cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 2)


class CartRemoveViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', slug='test-product',
                                              price=10.00, category=self.category)

    def test_cart_remove_view(self):
        client = Client()

        url = reverse('cart:cart_add', args=[self.product.id])
        client.post(url, {'quantity': 1, 'override': False})

        url = reverse('cart:cart_remove', args=[self.product.id])

        response = client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('cart:cart_detail'))

        cart = response.wsgi_request.session['cart']
        self.assertFalse(str(self.product.id) in cart)


class CartDetailViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', slug='test-product',
                                              price=10.00, category=self.category)

    def test_cart_detail_view(self):
        url = reverse('cart:cart_add', args=[self.product.id])

        self.client.post(url, {'quantity': 2, 'override': False})

        url = reverse('cart:cart_detail')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'cart/detail.html')

        self.assertIsNotNone(response.context['cart'])
        self.assertIsNotNone(response.context['coupon_apply_form'])
        self.assertIsNotNone(response.context['recommended_products'])

        self.assertEqual(len(response.context['cart']), 2)
        self.assertEqual(response.context['cart'].cart[str(self.product.id)]['product'], self.product)

        self.assertIsInstance(response.context['coupon_apply_form'], CouponApplyForm)

        self.assertIsInstance(response.context['recommended_products'], list)
