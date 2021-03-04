from django.urls import  path, re_path
from .views import dashboard_view

urlpatterns = [
    path('', dashboard_view, name="dashboard"),
] 