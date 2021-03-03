from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class SignUpForm(CustomUserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Please, provide a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', )