import random

from django.utils import timezone

from core.mailing import send_gmail
from draw.models import ActiveRaffleCampaign

def announce_if_winner():
    active_campaign = ActiveRaffleCampaign.object().campaign
    if timezone.now() >= active_campaign.end_date and not active_campaign.campaign_closed: # If End Time of a Campaign and Campaign Not Closed (campaign_closed: boolean field) do:
        winner_id = active_campaign.winning_ticket
        if not active_campaign.winning_ticket: # If no winner, choose winner
            ticket_set = active_campaign.ticket_set.all()
            if not len(ticket_set):
                return ""
            winner_id = random.choice(ticket_set).six_digit_id
            active_campaign.winning_ticket = winner_id
        # Send a mail to winner and close campaign
        send_gmail(f"Congratulations On Winning the Raffle Draw ({active_campaign.campaign_ref.upper()})",
        f"Your ticket: {active_campaign.campaign_ref.upper()}-{winner_id} was randomly selected as the winning ticket and you would receive the {active_campaign.prize.name} from Ralph.", 
        "pro.ajibolaojo@gmail.com")
        active_campaign.campaign_closed = True
        active_campaign.save()
