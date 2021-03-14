from django.contrib import admin
from .models import RaffleCampaign, Ticket, ActiveRaffleCampaign

admin.site.register(RaffleCampaign)
admin.site.register(Ticket)
admin.site.register(ActiveRaffleCampaign)
