from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Vehicle(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='vehicles',
        verbose_name=_('Owner')
    )

    make = models.CharField(
        max_length=30,
        verbose_name=_('Make'),
        null=False,
        blank=False
    )

    model = models.CharField(
        max_length=30,
        verbose_name=_('Model'),
        null=False,
        blank=False
    )

    reg_number = models.CharField(
        max_length=30,
        verbose_name=_('Registration number'),
        null=False,
        blank=False
    )

    image = models.ImageField(
        upload_to='vehicles/',
        verbose_name=_('Image'),
        null=True,
        blank=True
    )

    @property
    def vehicle_name(self):
        return f'{self.make} {self.model}'

    def __str__(self):
        return f'{self.make} {self.model} owned by {self.user}'

    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')
