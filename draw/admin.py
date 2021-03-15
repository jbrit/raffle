from django.contrib import admin
from .models import RaffleCampaign, Ticket, ActiveRaffleCampaign, Prize

admin.site.register(RaffleCampaign)
admin.site.register(Ticket)
admin.site.register(ActiveRaffleCampaign)
admin.site.register(Prize)
