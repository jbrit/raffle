from django.urls import  path, re_path
from .views import home_view, signup_view, activate, account_activation_sent, login_view, LogoutView

urlpatterns = [
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('account_activation_sent/', account_activation_sent, name="account_activation_sent"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]+)/$', activate, name='activate')
] 