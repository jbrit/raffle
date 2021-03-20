from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .mailing import send_gmail
from .managers import CustomUserManager
from .validators import validate_room

from wallet.models import Wallet

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def email_user(self, *args, **kwargs):
        send_gmail(
            '{}'.format(args[0]), # Subject
            '{}'.format(args[1]), # Message
            self.email,
            )


    def __str__(self):
        return self.email

       

class Profile(models.Model):

    halls = models.TextChoices("Hall", "Daniel Abraham Joseph Isaac Dorcas Sarah Abigail")
    levels = models.TextChoices("Level", "100 200 300 400 500")


    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField("First Name", blank=True, max_length=20)
    last_name = models.CharField("Last Name", blank=True, max_length=20)
    room_no = models.CharField("Room Number", validators=[validate_room], blank=True, max_length=4)
    department = models.CharField("Department", blank=True ,max_length=50)
    hall = models.CharField("Hall", choices=halls.choices, default=halls.choices[0][0], max_length=20)
    level = models.CharField("Level", choices=levels.choices, default=levels.choices[0][0], max_length=3)
    

    def get_full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        
    def __str__(self):
        return self.user.email

@receiver(post_save, sender=CustomUser)
def update_user_wallet_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(owner=instance)
    instance.profile.save()
    instance.wallet.save()


class LearnMore(models.Model):
    text = models.TextField()

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()


    def save(self, *args, **kwargs):
        if not self.pk and LearnMore.objects.exists():
            raise ValidationError("Only One learn more text can exist")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Learn More"

    class Meta:
        verbose_name_plural = "Learn More"