from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .managers import CustomUserManager

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
        send_mail(
            '{}'.format(args[0]), # Subject
            '{}'.format(args[1]), # Message
            settings.EMAIL_HOST_USER, # From mail
            [self.email],
            fail_silently=False,
            )


    def __str__(self):
        return self.email

       

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # create more user related info


@receiver(post_save, sender=CustomUser)
def update_user_wallet_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Wallet.objects.create(owner=instance)
    instance.profile.save()
    instance.wallet.save()
