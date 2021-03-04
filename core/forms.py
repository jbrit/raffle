from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models

from .models import CustomUser
from .validators import validate_room

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


halls = models.TextChoices("Hall", "Daniel Abraham Joseph Isaac Dorcas Sarah Abigail")
levels = models.TextChoices("Level", "100 200 300 400 500")


class SignUpForm(CustomUserCreationForm):
    first_name = forms.CharField(max_length=20, strip=True, help_text='First Name')
    last_name = forms.CharField(max_length=20, strip=True, help_text='Last Name')
    room_no = forms.CharField(min_length=4, max_length=4, strip=True, validators=[validate_room], help_text='Room Number')
    department = forms.CharField(max_length=50, help_text='Department')
    hall = forms.ChoiceField(choices=halls.choices)
    level = forms.ChoiceField(choices=levels.choices)
    email = forms.EmailField(max_length=254, help_text='Please, provide a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', )