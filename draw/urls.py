from django.urls import  path, re_path
from .views import  UserCampaignsView, UserCampaignDetailView, buy_ticket
urlpatterns = [
    path('campaigns/', UserCampaignsView.as_view(), name="campaigns"),
    re_path(r'^campaigns/rfc(?P<id>[0-9]{4})/$',UserCampaignDetailView.as_view(), name="campaign_detail"),
    re_path(r'^campaigns/rfc(?P<id>[0-9]{4})/buy$', buy_ticket, name="buy_ticket"),
] 