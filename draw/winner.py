from django.utils import timezone

from core.mailing import send_gmail
from draw.models import ActiveRaffleCampaign

def announce_if_winner():
    active_campaign = ActiveRaffleCampaign.object().campaign
    if timezone.now() >= active_campaign.end_date and not active_campaign.campaign_closed:
        if not active_campaign.winning_ticket:
            pass
    send_gmail("Cron Job", "This is a django cron job", "pro.ajibolaojo@gmail.com")
    # If End Time of a Campaign <= 1:00 and Campaign Not Closed (campaign_closed: boolean field) do:
    # If no winner, choose winner
    # Send a mail to the winner