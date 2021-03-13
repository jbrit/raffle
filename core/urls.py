from django.urls import  path
from .views import home_view, signup_view, SettingsView, EditProfileView, change_password, activate, account_activation_sent, login_view, LogoutView

urlpatterns = [
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('account_activation_sent/', account_activation_sent, name="account_activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('dashboard/settings/', SettingsView.as_view(), name='settings'),
    path('dashboard/settings/editprofile', EditProfileView.as_view(), name='edit_profile'),
    path('dashboard/settings/changepassword', change_password, name='change_password'),
] 