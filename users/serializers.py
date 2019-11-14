from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def validate_birth_date(self, value):
        if value:
            if value > date.today():
                raise serializers.ValidationError(
                    'Birth date cannot be in the future'
                )
            age = relativedelta(date.today(), value).years
            if age < 18:
                raise serializers.ValidationError(
                    'User should be 18 years or older'
                )
        return value

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
            'birth_date',
            'url',
        ]
