from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from places.models import Place
from vehicles.models import Vehicle
from .models import Trip

User = get_user_model()

class TripTests(TestCase):

    def setUp(self):
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
        self.assertEqual(error.message, 'Origin and destination cannot be the same')
