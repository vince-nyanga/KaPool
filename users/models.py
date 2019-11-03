from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

GENDER_OPTIONS = (
    ('female', 'Female'),
    ('male', 'Male'),
    ('wont-say', "Won't say"),
)

class User(AbstractUser):
    """
    Custom user model to replace the one provided by django
    """
    gender = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        choices=GENDER_OPTIONS,
        default='wont-say',
        verbose_name=_('Gender'),
        help_text=_("User's gender")
    )

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date of birth'),
        help_text=_('Date of birth')
    )
    

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
