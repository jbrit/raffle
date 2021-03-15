from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from draw.models import ActiveRaffleCampaign

# Create your views here.
@login_required(login_url="/login/")
def dashboard_view(request):
    active_raffle = ActiveRaffleCampaign.object()
    context = {"active_raffle": active_raffle}
    return render(request, "core/dashboard_home.html", context=context)