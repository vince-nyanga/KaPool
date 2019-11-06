from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase


class UserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'vince')
        self.assertEqual(user.email, 'vince@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'vince')
        self.assertEqual(user.email, 'vince@test.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_younger_than_18_should_raise(self):
        User = get_user_model()
        with self.assertRaises(ValidationError) as cm:
            user = User.objects.create_superuser(
                username='vince',
                email='vince@test.com',
                password='testpass123',
                birth_date=date.today()
            )
        error = cm.exception
        self.assertEqual(error.message, 'User should be 18 years or older')

    def test_create_user_future_birth_date_should_raise(self):
        User = get_user_model()
        next_year = date.today() + relativedelta(years=1)

        with self.assertRaises(ValidationError) as cm:
            user = User.objects.create_superuser(
                username='vince',
                email='vince@test.com',
                password='testpass123',
                birth_date=next_year
            )
        error = cm.exception
        self.assertEqual(error.message, 'Birth date cannot be in the future')
