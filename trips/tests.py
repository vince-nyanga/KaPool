from datetime import date
import json
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from places.models import Place
from vehicles.models import Vehicle
from .models import Trip

User = get_user_model()


def create_data():
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

    origin = Place(name='Origin')
    origin.save()

    destination = Place(name='Destination')
    destination.save()


class TripTests(TestCase):

    def setUp(self):
        create_data()

    def test_create_trip(self):
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        self.assertEqual(trip.user.username, 'vince')
        self.assertEqual(trip.origin.name, 'Origin')
        self.assertEqual(trip.destination.name, 'Destination')

    def test_date_in_past_should_raise(self):
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)
        trip_date = date.today() + relativedelta(days=-1)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=trip_date
        )
        with self.assertRaises(ValidationError) as cm:
            trip.save()
        error = cm.exception
        self.assertEqual(error.message, 'Trip date cannot be in the past')

    def test_same_origin_and_destination_should_raise(self):
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=1)
        trip_date = date.today()

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=trip_date
        )
        with self.assertRaises(ValidationError) as cm:
            trip.save()
        error = cm.exception
        self.assertEqual(
            error.message, 'Origin and destination cannot be the same')


class TripApiTest(APITestCase):

    def test_get_trips(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        response = self.client.get('/api/v1/trips/')
        self.assertEqual(json.loads(response.content), [
            {
                "id": 1,
                "url": "http://testserver/api/v1/trips/1/",
                "trip_date": str(date.today()),
                "num_seats": 1,
                "origin": {
                    "id": 1,
                    "name": "Origin"
                },
                "destination": {
                    "id": 2,
                    "name": "Destination"
                },
                "vehicle": {
                    "id": 1,
                    "url": "http://testserver/api/v1/vehicles/1/",
                    "make": "Make",
                    "model": "Model",
                    "reg_number": "1234",
                    "image": None,
                    "owner_url": "http://testserver/api/v1/users/1/"
                },
                "driver": {
                    "username": "vince",
                    "email": "vince@test.com",
                    "first_name": "",
                    "last_name": "",
                    "gender": "wont-say",
                    "birth_date": None,
                    "url": "http://testserver/api/v1/users/1/",
                    "profile_pic": None
                }
            }

        ])

    def test_create_trip(self):
        create_data()
        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/v1/trips/', {
            'trip_date': str(date.today()),
            'origin_id': 1,
            'destination_id': 2,
            'vehicle_id': 1
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        trip = Trip.objects.get(pk=1)
        self.assertEqual(trip.origin.name, 'Origin')
        self.assertEqual(trip.destination.name, 'Destination')
        self.assertEqual(trip.trip_date, date.today())
        self.assertEqual(trip.user, user)

    def test_update_trip_unauthenticated_forbidden(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        tomorrow = date.today() + relativedelta(days=1)

        response = self.client.put('/api/v1/trips/1/', {
            'trip_date': str(tomorrow),
            'origin_id': 1,
            'destination_id': 2,
            'vehicle_id': 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_other_users_trip_forbidden(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        user2 = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@email.com'
        )
        self.client.force_authenticate(user=user2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        tomorrow = date.today() + relativedelta(days=1)

        response = self.client.put('/api/v1/trips/1/', {
            'trip_date': str(tomorrow),
            'origin_id': 1,
            'destination_id': 2,
            'vehicle_id': 1
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_trip(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        self.client.force_authenticate(user=user)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        tomorrow = date.today() + relativedelta(days=1)

        response = self.client.put('/api/v1/trips/1/', {
            'trip_date': str(tomorrow),
            'origin_id': 1,
            'destination_id': 2,
            'vehicle_id': 1
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        trip = Trip.objects.get(pk=1)
        self.assertEqual(trip.trip_date, tomorrow)

    def test_delete_trip_unathenticated_forbidden(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        response = self.client.delete('/api/v1/trips/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_users_trip_forbidden(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        user2 = User.objects.create_user(
            username='test',
            password='testpass123',
            email='test@email.com'
        )
        self.client.force_authenticate(user=user2)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        response = self.client.delete('/api/v1/trips/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_trip(self):
        create_data()
        user = User.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)
        origin = Place.objects.get(pk=1)
        destination = Place.objects.get(pk=2)

        self.client.force_authenticate(user=user)

        trip = Trip(
            user=user,
            origin=origin,
            destination=destination,
            vehicle=vehicle,
            trip_date=date.today()
        )
        trip.save()

        response = self.client.delete('/api/v1/trips/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Trip.objects.all().count(), 0)
