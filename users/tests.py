from datetime import date
import json
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


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


class UserApiTest(APITestCase):
    def test_list_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            first_name='Vincent',
            last_name='Nyanga',
            password='testpass123'
        )
        response = self.client.get('/api/v1/users/')
        self.assertEqual(json.loads(response.content), [{
            'username': 'vince',
            'email': 'vince@test.com',
            'first_name': 'Vincent',
            'last_name': 'Nyanga',
            'gender': 'wont-say',
            'birth_date': None,
            'url': 'http://testserver/api/v1/users/1/',
            'profile_pic': None
        }])

    def test_get_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            first_name='Vincent',
            last_name='Nyanga',
            password='testpass123'
        )
        response = self.client.get('/api/v1/users/1/')
        self.assertEqual(json.loads(response.content), {
            'username': 'vince',
            'email': 'vince@test.com',
            'first_name': 'Vincent',
            'last_name': 'Nyanga',
            'gender': 'wont-say',
            'birth_date': None,
            'url': 'http://testserver/api/v1/users/1/',
            'profile_pic': None
        })

    def test_update_user_unauthenticated_forbidden(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            first_name='Vincent',
            last_name='Nyanga',
            password='testpass123'
        )
        response = self.client.put('/api/v1/users/1/', {
            'username': 'vince',
            'email': 'vince@test.com',
            'first_name': 'Vincent',
            'last_name': 'Nyanga',
            'gender': 'male',
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_other_users_profile_forbidden(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            first_name='Vincent',
            last_name='Nyanga',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@email.com'
        )

        self.client.force_authenticate(user=user2)
        
        response = self.client.put('/api/v1/users/1/', {
            'username': 'vince',
            'email': 'vince@test.com',
            'first_name': 'Vincent',
            'last_name': 'Nyanga',
            'gender': 'male',
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            first_name='Vincent',
            last_name='Nyanga',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        response = self.client.put('/api/v1/users/1/', {
            'username': 'vince',
            'email': 'vince@test.com',
            'first_name': 'Vincent',
            'last_name': 'Nyanga',
            'gender': 'male',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
            'username': 'vince',
            'email': 'vince@test.com',
            'first_name': 'Vincent',
            'last_name': 'Nyanga',
            'gender': 'male',
            'birth_date': None,
            'url': 'http://testserver/api/v1/users/1/',
            'profile_pic': None
        })

    def test_delete_not_allowed(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            first_name='Vincent',
            last_name='Nyanga',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        response = self.client.delete('/api/v1/users/1/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
