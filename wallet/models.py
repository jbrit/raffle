from django.db import models
from django.conf import settings

class Wallet(models.Model):
    balance = models.FloatField(default=0)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="wallet", on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.email