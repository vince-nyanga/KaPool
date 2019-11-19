from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from places.models import Place
from vehicles.models import Vehicle


class Trip(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='trips',
        verbose_name=_('Driver'),
    )

    origin = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='trip_origins',
        verbose_name=_('From')
    )

    destination = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='trip_destinations',
        verbose_name=_('To')
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='trip_vehicles',
        verbose_name=_('Vehicle')
    )

    trip_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('Trip date')
    )

    num_seats  = models.IntegerField(
        default=1,
        verbose_name=_('Number of seats'),
        help_text=_('Number of seats available')
    )

    def save(self, *args, **kwargs):
        if self.origin == self.destination:
            raise ValidationError(
                'Origin and destination cannot be the same'
            )
        if self.trip_date < date.today():
            raise ValidationError(
                'Trip date cannot be in the past'
            )
        super(Trip, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.origin} to {self.destination} by {self.user}'

    class Meta:
        verbose_name = _('Trip')
        verbose_name_plural = _('Trips')
        ordering = ['trip_date']
