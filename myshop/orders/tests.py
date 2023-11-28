from decimal import Decimal, ROUND_HALF_UP

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from coupons.models import Coupon
from orders.models import Order, OrderItem
from shop.models import Category, Product


class OrderModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=Decimal(19.99)
        )

        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            discount=20,
            active=True
        )

        self.order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            address='123 Main St',
            postal_code='12345',
            city='Cityville',
            coupon=self.coupon,
            discount=self.coupon.discount,
        )
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, price=self.product.price,
                                                   quantity=2)

    def test_order_str_method(self):
        # Ensure that the __str__ method returns the expected string representation.
        self.assertEqual(str(self.order), f'Order {self.order.id}')

    def test_order_get_total_cost(self):
        """
        Test the get_total_cost method of the Order model.

        Ensure that the get_total_cost method returns the expected total cost after discount.
        """

        # Assuming you have an OrderItem model with a get_cost method

        total_before_discount = self.order_item.price * self.order_item.quantity
        expected_total_cost = total_before_discount - total_before_discount * (self.order.discount / Decimal(100))
        expected_total_cost = expected_total_cost.quantize(Decimal('0.000'), rounding=ROUND_HALF_UP)
        self.assertEqual(self.order.get_total_cost(), expected_total_cost)

    def test_order_get_total_cost_before_discount(self):
        """
        Test the get_total_cost_before_discount method of the Order model.

        Ensure that the get_total_cost_before_discount method returns the expected total cost before discount.
        """
        # Assuming you have an OrderItem model with a get_cost method
        expected_total_cost = self.order_item.price * self.order_item.quantity
        expected_total_cost = expected_total_cost.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        self.assertEqual(self.order.get_total_cost_before_discount(), expected_total_cost)

    def test_order_get_discount(self):
        """
        Test the get_discount method of the Order model.

        Ensure that the get_discount method returns the expected discount value.
        """
        # Assuming you have an OrderItem model with a get_cost method
        expected_discount = self.order.get_total_cost_before_discount() * (Decimal(self.order.discount) / Decimal(100))
        self.assertEqual(self.order.get_discount(), expected_discount)


class OrderCreateViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=Decimal('10.00'),
        )

        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )

    def test_order_create_view_get(self):
        url = reverse('orders:order_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order/create.html')
        self.assertIsNotNone(response.context['form'])

    def test_order_create_view_post_valid_data(self):
        url = reverse('cart:cart_add', args=[self.product.id])
        self.client.post(url, {'quantity': 2, 'override': False})

        url = reverse('orders:order_create')
        response = self.client.post(url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '123 Main St',
            'postal_code': '12345',
            'city': 'City'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('payment:process'))
        self.assertTrue(Order.objects.exists())
        self.assertTrue(OrderItem.objects.exists())
        self.assertIsNotNone(self.client.session.get('order_id'))

        with self.assertRaises(TypeError) as context:
            cart = response.context['cart']

    def test_order_create_view_post_invalid_data(self):
        url = reverse('orders:order_create')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'orders/order/create.html')
        self.assertIsNotNone(response.context['form'])
        self.assertIsNone(self.client.session.get('order_id'))
