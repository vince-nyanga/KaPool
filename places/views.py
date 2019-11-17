from django.shortcuts import render
from rest_framework import viewsets, mixins

from .models import Place
from .serializers import PlaceSerializer

class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
