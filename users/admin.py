from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    """
    Custom user admin
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username','first_name', 'last_name', 'email', 'gender', 'birth_date']
    add_fieldsets = (
            (
                'User info',
                {
                    'classes': ('wide',),
                    'fields': ('username','email', 'password1', 'password2', 'gender', 'birth_date'),
                },
            ),
    )

    fieldsets = (
            (
                'User info',
                {
                    'classes': ('wide',),
                    'fields': ('username','email', 'gender', 'birth_date'),
                },
            ),
    )


admin.site.register(CustomUser, CustomUserAdmin) 
