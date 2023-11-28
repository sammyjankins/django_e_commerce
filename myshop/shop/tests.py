from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from shop.models import Category, Product


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_category_str_method(self):
        # Ensure that the __str__ method returns the expected string representation.
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_get_absolute_url_method(self):
        # Ensure that the get_absolute_url method returns the expected URL.
        expected_url = reverse('shop:product_list_by_category', args=['test-category'])
        self.assertEqual(self.category.get_absolute_url(), expected_url)

    def test_category_ordering(self):
        """
        Test the ordering of categories based on the 'name' field.

        Ensure that categories are sorted in alphabetical order.
        """

        Category.objects.create(name='Category B', slug='category-b')
        Category.objects.create(name='Category A', slug='category-a')

        categories = list(Category.objects.values_list('name', flat=True))

        self.assertEqual(categories, ['Category A', 'Category B', 'Test Category'])

    def test_category_slug_unique_constraint(self):
        """
        Ensure that attempting to create a category with a duplicate slug raises an IntegrityError.
        """

        duplicate_category = Category(name='Duplicate Category', slug='test-category')
        with self.assertRaises(Exception) as context:
            duplicate_category.save()

        self.assertIn('duplicate key value', str(context.exception))


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=19.99
        )

    def test_product_str_method(self):
        # Ensure that the __str__ method returns the expected string representation.
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_get_absolute_url_method(self):
        # Ensure that the get_absolute_url method returns the expected URL.
        expected_url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), expected_url)

    def test_product_ordering(self):
        """
        Test the ordering of products based on the 'name' field.

        Ensure that products are sorted in alphabetical order.
        """
        Product.objects.create(category=self.category, name='Product B', slug='product-b', price=29.99)
        Product.objects.create(category=self.category, name='Product A', slug='product-a', price=19.99)

        products = list(Product.objects.values_list('name', flat=True))

        self.assertEqual(products, ['Product A', 'Product B', 'Test Product'])

    def test_product_price_decimal_places(self):
        """
        Test the decimal places for the 'price' field of the Product model.

        Ensure that the 'price' field has the correct number of decimal places.
        """
        retrieved_product = Product.objects.get(id=self.product.id)

        self.assertEqual(retrieved_product.price, Decimal('19.99'))

    def test_product_available_default_value(self):
        """
        Test the default value for the 'available' field of the Product model.

        Ensure that the 'available' field is set to True by default.
        """
        retrieved_product = Product.objects.get(id=self.product.id)

        self.assertTrue(retrieved_product.available)


class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=19.99
        )

    def test_product_detail_view(self):
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'shop/product/detail.html')

        self.assertEqual(response.context['product'], self.product)


class ProductListViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            price=19.99
        )

    def test_product_list_view_without_category(self):
        url = reverse('shop:product_list')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertIsNone(response.context['category'])
        self.assertIsNotNone(response.context['categories'])
        self.assertIsNotNone(response.context['products'])

    def test_product_list_view_with_category(self):
        url = reverse('shop:product_list_by_category', args=[self.category.slug])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertIsNotNone(response.context['category'])
        self.assertIsNotNone(response.context['categories'])
        self.assertIsNotNone(response.context['products'])
        self.assertEqual(response.context['category'], self.category)
        self.assertIn(self.product, response.context['products'])
