from django.shortcuts import render

# Create your views here.
def balance_view(request):
    return render(request, "wallet/balance.html")