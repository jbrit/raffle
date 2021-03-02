from django.db import models
from django.conf import settings

class Transaction(models.Model):
    amount = models.FloatField()
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transaction", on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False) 

class Wallet(models.Model):
    balance = models.FloatField(default=0)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="wallet", on_delete=models.CASCADE)
