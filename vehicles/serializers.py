from rest_framework import serializers

from .models import Vehicle

class VehicleSerializer(serializers.HyperlinkedModelSerializer):
    owner_url = serializers.HyperlinkedRelatedField(
        source='user',
        view_name='user-detail',
        read_only=True
    )
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'url',
            'make',
            'model',
            'reg_number',
            'image',
            'owner_url',
        ]