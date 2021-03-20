from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Prize(models.Model):
    img_url = models.URLField(blank=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} | {self.description}"


class RaffleCampaign(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ticket_price = models.FloatField(default=200.0)
    winning_ticket = models.CharField(blank=True, validators=[], max_length=16) # TODO: Winning Ticket Validator
    prize = models.ForeignKey(Prize, null=True, on_delete=models.SET_NULL)
    campaign_closed = models.BooleanField(default=False)

    @property
    def campaign_ref(self):
        return f"rfc{self.id:04d}"
    
    @property
    def four_digit_id(self):
        return f"{self.id:04d}"

    @property
    def is_active(self):
        return self.end_date > timezone.now() and self.start_date <= timezone.now()

    
    # Check if a user can buy a campaign ticket
    def can_buy_ticket(self, user):
        # Check if the user has money and the campaign is valid
        return self.ticket_price <= user.wallet.balance and self.is_active

    def buy_ticket(self, user):
        if self.can_buy_ticket(user):
            user.wallet.balance -= self.ticket_price
            user.save()
            Ticket.objects.create(campaign=self, buyer=user)

    def clean(self, *args, **kwargs):
        if self.start_date >= self.end_date:
            raise ValidationError({
                    'end_date': _('End date should come after the start date'),
                })
        if self.winning_ticket != "" and not self.ticket_set.filter(id=self.winning_ticket).exists():
            raise ValidationError({
                    'winning_ticket': _('The winning ticket must be from this raffle campaign'),
                })

    def __str__(self):
        return self.campaign_ref

        

class Ticket(models.Model):
    campaign = models.ForeignKey(RaffleCampaign, editable=False, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE)
    # ticket_ref = models.CharField(max_length=20, unique=True, editable=False)

    @property
    def ticket_ref(self):
        return f"{self.campaign.campaign_ref}-{self.id:06d}"

    @property
    def is_winning(self):
        return self.campaign.winning_ticket == self.ticket_ref

    @property
    def six_digit_id(self):
        return f"{self.id:06d}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer.email} {self.ticket_ref}"


class ActiveRaffleCampaign(models.Model):
    campaign = models.OneToOneField(RaffleCampaign, null=True, on_delete=models.SET_NULL)

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()

    @property
    def is_upcoming(self):
        return self.campaign.start_date > timezone.now()

    @property
    def is_current(self):
        return self.campaign.start_date <= timezone.now() and self.campaign.end_date >= timezone.now()

    @property
    def is_past(self):
        return self.campaign.end_date < timezone.now()

    def save(self, *args, **kwargs):
        if not self.pk and ActiveRaffleCampaign.objects.exists():
            raise ValidationError("Only One active campaign can exist")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Active Raffle Campaign"

    class Meta:
        verbose_name_plural = "Active Raffle Campaign"


class UpcomingRaffleCampaign(models.Model):
    campaign = models.OneToOneField(RaffleCampaign, null=True, on_delete=models.SET_NULL)

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()

    @property
    def is_upcoming(self):
        return self.campaign.start_date > timezone.now()

    @property
    def is_current(self):
        return self.campaign.start_date <= timezone.now() and self.campaign.end_date >= timezone.now()

    @property
    def is_past(self):
        return self.campaign.end_date < timezone.now()

    def save(self, *args, **kwargs):
        if not self.pk and UpcomingRaffleCampaign.objects.exists():
            raise ValidationError("Only One upcoming campaign can exist")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Upcoming Raffle Campaign"

    class Meta:
        verbose_name_plural = "Upcoming Raffle Campaign"