from django.db import models
from django.utils.translation import ugettext_lazy as _


class Place(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Place')
        verbose_name_plural = _('Places')
        ordering = ['name',]
