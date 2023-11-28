from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from coupons.models import Coupon


class CouponModelTest(TestCase):

    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            discount=20,
            active=True
        )

    def test_coupon_str_method(self):
        self.assertEqual(str(self.coupon), 'TESTCODE')

    def test_coupon_code_unique_constraint(self):
        """
        Test the unique constraint on the 'code' field of the Coupon model.

        Ensure that attempting to create a coupon with a duplicate code raises an IntegrityError.
        """
        duplicate_coupon = Coupon(
            code='TESTCODE',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=7),
            discount=30,
            active=True
        )
        with self.assertRaises(Exception) as context:
            duplicate_coupon.save()

        self.assertIn('duplicate key value', str(context.exception))


class CouponApplyViewTest(TestCase):

    def setUp(self):
        self.valid_coupon = Coupon.objects.create(
            code='VALIDCODE',
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            discount=10,
            active=True
        )

        self.invalid_coupon = Coupon.objects.create(
            code='INVALIDCODE',
            valid_from=timezone.now() - timezone.timedelta(days=2),
            valid_to=timezone.now() - timezone.timedelta(days=1),
            discount=20,
            active=False
        )

    def test_coupon_apply_view_with_valid_code(self):
        url = reverse('coupons:apply')
        response = self.client.post(url, {'code': 'VALIDCODE'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))
        self.assertEqual(self.client.session['coupon_id'], self.valid_coupon.id)

    def test_coupon_apply_view_with_invalid_code(self):
        url = reverse('coupons:apply')
        response = self.client.post(url, {'code': 'INVALIDCODE'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))
        self.assertIsNone(self.client.session.get('coupon_id'))
