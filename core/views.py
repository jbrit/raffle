from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from core.forms import SignUpForm
from core.tokens import account_activation_token
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.decorators import login_required, user_passes_test


# No logged in user
def logged_out_user(user):
    return not user.is_authenticated

def home_view(request):
    return render(request,"core/home.html")


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
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class SettingsView(TemplateView):
    template_name = 'core/settings.html'