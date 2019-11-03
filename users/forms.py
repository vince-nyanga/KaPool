from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form
    """

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('gender', 'birth_date')


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form
    """

    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('gender', 'birth_date')
