from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class RaffleCampaign(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winning_ticket = models.CharField(blank=True, max_length=20)

    @property
    def campaign_ref(self):
        return f"rfc{self.id}"

    @property
    def is_active(self):
        return self.end_date < timezone.now()

    def clean(self, *args, **kwargs):
        if self.start_date >= self.end_date:
            raise ValidationError({
                    'end_date': _('End date should come after the start date'),
                })

    def __str__(self):
        return self.campaign_ref

        

class Ticket(models.Model):
    campaign = models.ForeignKey(RaffleCampaign, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_ref = models.CharField(max_length=20, unique=True, editable=False)

    def is_winning(self):
        return self.campaign.winning_ticket == self.ticket_ref

    def save(self, *args, **kwargs):
        if self.ticket_ref == "":
            # Generate unique ticket number
            self.ticket_ref = f"{self.campaign.campaign_ref}-{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer.email} {self.id}"