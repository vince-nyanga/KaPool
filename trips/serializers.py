from datetime import date
from rest_framework import serializers

from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from places.models import Place
from places.serializers import PlaceSerializer
from users.serializers import UserSerializer
from .models import Trip


class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Filters `PrimaryKeyRelatedField` based on the logged in user.

    See  https://stackoverflow.com/questions/27947143
    """

    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(
            UserFilteredPrimaryKeyRelatedField,
            self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)


class TripSerializer(serializers.HyperlinkedModelSerializer):
    origin_id = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        source='origin',
        write_only=True
    )

    origin = PlaceSerializer(read_only=True)

    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        source='destination',
        write_only=True

    )
    destination = PlaceSerializer(read_only=True)

    vehicle_id = UserFilteredPrimaryKeyRelatedField(
        queryset=Vehicle.objects,
        source='vehicle',
        write_only=True
    )

    vehicle = VehicleSerializer(read_only=True)

    driver = UserSerializer(source='user', read_only=True)

    def validate_trip_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                'Trip date cannot be in the past')
        return value

    def validate(self, data):
        if data['origin'] == data['destination']:
            raise serializers.ValidationError(
                'Origin and destination cannot be the same')

        return data

    class Meta:
        model = Trip
        fields = [
            'id',
            'url',
            'trip_date',
            'num_seats',
            'origin_id',
            'origin',
            'destination_id',
            'destination',
            'vehicle_id',
            'vehicle',
            'driver',
        ]
