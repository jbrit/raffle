from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def dashboard_view(request):
    tickets = request.user.ticket_set.all()
    return render(request, "core/dashboard_home.html")