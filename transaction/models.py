from django.db import models
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone

from .flutterwave import get_payment_url, verify as flutterwave_verify


class Transaction(models.Model):
    amount = models.FloatField()
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="transaction", on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    generated = models.DateTimeField(auto_now_add=True)

    def verify(self, tx_id):
        if not self.is_verified:
            if flutterwave_verify(self, tx_id):
                self.is_verified = True
                self.save()
                self.made_by.wallet.balance += self.amount
                self.made_by.save()
    
    def get_payment_data(self, request):
       redirect_url = f"http://{get_current_site(request).domain}{reverse('transaction_verify', kwargs={'id':self.eight_digit_id})}"
       data = get_payment_url(self,self.made_by, redirect_url)  # link, successful
       return data["link"]
       

    @property
    def tx_ref(self):
        if not settings.FLUTTERWAVE_PRODUCTION:
            return f"rftx-test-{self.id:08d}-{settings.ENV_ID}"
        return f"rftx-{self.id:08d}-{settings.ENV_ID}"

    @property
    def eight_digit_id(self):
        return f"{self.id:08d}"