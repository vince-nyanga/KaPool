import json
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Vehicle


User = get_user_model()


class VehicleApiTests(APITestCase):
    def test_list_vehicles(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )

        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()

        response = self.client.get('/api/v1/vehicles/')
        self.assertEqual(json.loads(response.content), [
            {
                'id': 1,
                'url': 'http://testserver/api/v1/vehicles/1/',
                'make': 'Make',
                'model': 'Model',
                'reg_number': '1234',
                'image': None,
                'owner_url': 'http://testserver/api/v1/users/1/'
            }
        ])

    def test_add_vehicle_unathenticated_forbidden(self):
        response = self.client.post('/api/v1/vehicles/', {
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1234',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_vehicle(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/v1/vehicles/', {
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1234',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content), {
            'id': 1,
            'url': 'http://testserver/api/v1/vehicles/1/',
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1234',
            'image': None,
            'owner_url': 'http://testserver/api/v1/users/1/'
        })

    def test_update_vehicle_unauthenticated_forbidden(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )

        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()

        response = self.client.put('/api/v1/vehicles/1/', {
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1235',
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_other_users_vehicle_forbidden(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )

        user2 = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@email.com'
        )

        self.client.force_authenticate(user=user2)

        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()

        response = self.client.put('/api/v1/vehicles/1/', {
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1235',
        })

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_vehicle(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)

        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()

        response = self.client.put('/api/v1/vehicles/1/', {
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1235',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {
            'id': 1,
            'url': 'http://testserver/api/v1/vehicles/1/',
            'make': 'Make',
            'model': 'Model',
            'reg_number': '1235',
            'image': None,
            'owner_url': 'http://testserver/api/v1/users/1/'
        })

    def test_delete_unauthenticated_forbidden(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()
        response = self.client.delete('/api/v1/vehicles/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_users_vehicle_forbidden(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@email.com'
        )

        self.client.force_authenticate(user=user2)
        
        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()
        response = self.client.delete('/api/v1/vehicles/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vehicle(self):
        user = User.objects.create_user(
            username='vince',
            email='vince@test.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)

        vehicle = Vehicle(
            make='Make',
            model='Model',
            reg_number='1234',
            user=user
        )
        vehicle.save()
        response = self.client.delete('/api/v1/vehicles/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.all().count(), 0)
