from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'brokerage')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'brokerage', 'is_active', 'is_staff', 'is_superuser')
