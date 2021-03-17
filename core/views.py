from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from core.forms import SignUpForm
from core.tokens import account_activation_token
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import RedirectView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, CustomUser
from draw.models import ActiveRaffleCampaign, UpcomingRaffleCampaign, Prize, Ticket
from draw.winner import announce_if_winner
from .mixins import CustomLoginRequiredMixin


# No logged in user
def logged_out_user(user):
    return not user.is_authenticated

def home_view(request):
    active_raffle = ActiveRaffleCampaign.object()
    upcoming_raffle = UpcomingRaffleCampaign.object()
    countdown_message = "Countdown to the next Raffle Draw" if active_raffle.is_upcoming else "Countdown to the end of Raffle Draw"
    raffle_prize_title = "Upcoming Raffle Prize" if active_raffle.is_upcoming else "Current Raffle Prize"
    countdown_time = active_raffle.campaign.end_date
    upcoming_time = upcoming_raffle.campaign.start_date
    prize_urls = list(map(lambda prize: prize.img_url, Prize.objects.all()))
    context = {
        "active_raffle": active_raffle,
        "upcoming_raffle": upcoming_raffle,
        "countdown_message": countdown_message,
        "countdown_time": countdown_time,
        "upcoming_time": upcoming_time,
        "raffle_prize_title": raffle_prize_title,
        "additional_countdown_message": "",
        "prize_urls": prize_urls
    }
    return render(request,"core/home.html",context)

def get_winner(request):
    announce_if_winner()
    active_campaign = ActiveRaffleCampaign.object().campaign
    if active_campaign.end_date > timezone.now():
        raise Http404("The Winner Cannot Be Generated")
    ticket = get_object_or_404(Ticket, id=active_campaign.winning_ticket)
    return HttpResponse(ticket.buyer.profile.get_full_name())

@user_passes_test(logged_out_user,"/", redirect_field_name=None)
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # Profile fields
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.room_no = form.cleaned_data.get('room_no')
            user.profile.department = form.cleaned_data.get('department')
            user.profile.hall = form.cleaned_data.get('hall')
            user.profile.level = form.cleaned_data.get('level')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Raffle Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
            pass
            # TODO: Invalid form 
    else:
        form = SignUpForm()
    
    return render(request, 'core/signup.html', {'form': form})



User = get_user_model()

@user_passes_test(logged_out_user,"/", redirect_field_name=None)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

@user_passes_test(logged_out_user,"/", redirect_field_name=None)
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

@user_passes_test(logged_out_user,"/", redirect_field_name=None)
def login_view(request):
    context = {}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next","/dashboard/")
            return redirect(next_url) # user dashboard
        else:
            context.update({"error": "Could not authenticate user!"})
    return render(request, 'core/login.html', context=context)


class LogoutView(RedirectView):
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class SettingsView(CustomLoginRequiredMixin, RedirectView):
    url = reverse_lazy("edit_profile")

class EditProfileView(CustomLoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["first_name", "last_name", "room_no", "department", "hall", "level"]
    template_name = 'core/editprofile.html'
    success_url = reverse_lazy("settings")
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.profile


class ChangePasswordView(CustomLoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'core/changepassword.html'
    success_url = reverse_lazy("change_password")
    form_class = PasswordChangeForm

    def get_object(self, queryset=None):
        return self.request.user

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'core/changepassword.html', {
        'form': form
    })