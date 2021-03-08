from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from core.mixins import CustomLoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import Http404

from .models import RaffleCampaign, Ticket


class UserCampaignsView(CustomLoginRequiredMixin, ListView):
    model = RaffleCampaign
    context_object_name = 'active_campaigns'
    template_name = "draw/campaigns.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['past_campaigns'] = RaffleCampaign.objects.filter(end_date__lte=timezone.now())
        return context
    
    def get_queryset(self):
        return RaffleCampaign.objects.filter(end_date__gt=timezone.now())


class UserCampaignDetailView(CustomLoginRequiredMixin, DetailView):
    model = RaffleCampaign
    pk_url_kwarg = "id"
    context_object_name = 'campaign'
    template_name = "draw/campaign_detail.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        campaign = self.get_object()
        context['can_buy_ticket'] = campaign.can_buy_ticket(self.request.user)
        context['user_tickets'] = Ticket.objects.filter(buyer=self.request.user, campaign=campaign)
        return context


@login_required
def buy_ticket(request, id):
    campaign_instance = get_object_or_404(RaffleCampaign, id=int(id))
    if request.method == "POST" and campaign_instance.can_buy_ticket(request.user):
        campaign_instance.buy_ticket(request.user)
        return redirect("campaign_detail", id=id)
    raise Http404("Could not process request")
    