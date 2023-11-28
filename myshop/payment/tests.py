from decimal import Decimal
from unittest.mock import Mock, patch

from django.http import Http404
from django.test import TestCase, RequestFactory
from django.urls import reverse, NoReverseMatch

from orders.models import Order, OrderItem
from payment.views import payment_process
from shop.models import Product, Category


class PaymentProcessViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=Decimal('10.00'),
        )

        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            postal_code='12345',
            city='Cityville',
        )
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, price=self.product.price,
                                                   quantity=2)

    def test_payment_process_view_get(self):
        request = self.factory.get(reverse('payment:process'))
        request.session = {'order_id': self.order.id}
        response = payment_process(request)

        self.assertEqual(response.status_code, 200)

    def test_payment_process_no_order_id_in_session(self):
        request = self.factory.get(reverse('payment:process'))
        request.session = {}
        with self.assertRaises(Http404) as context:
            response = payment_process(request)

    @patch('stripe.checkout.Session.create')
    @patch('stripe.Coupon.create')
    def test_payment_process_successful(self, mock_coupon_create, mock_session_create):
        request = self.factory.post(reverse('payment:process'))
        fake_session_object = Mock()
        fake_session_object.url = 'fake_session_url'

        mock_session_create.return_value = fake_session_object

        request.session = {'order_id': self.order.id}

        with self.assertRaises(NoReverseMatch) as context:
            response = payment_process(request)
