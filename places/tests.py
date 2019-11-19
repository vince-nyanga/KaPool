import json
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Place


class PlaceApiTest(APITestCase):
    def test_list_places(self):
        place = Place(name='Pretoria')
        place.save()

        response = self.client.get('/api/v1/places/')
        self.assertEqual(json.loads(response.content), [
            {
                'id': 1,
                'name': 'Pretoria'
            }
        ])

    def test_get_place(self):
        place = Place(name='Pretoria')
        place.save()
        response = self.client.get('/api/v1/places/1/')
        self.assertEqual(json.loads(response.content), {
            'id': 1,
            'name': 'Pretoria'
        })
