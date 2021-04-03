import requests
from django.conf import settings

PAYSTACK_PAYMENT_ENDPOINT = "https://api.paystack.co/transaction/initialize"

def get_payment_url(transaction, user, redirect_url):
    json_data = {
        "amount": f"{transaction.amount*100}",
        "callback_url": f"{redirect_url}",
        "email": f"{user.email}",
        
    }
    context = {'successful': False, 'link': '' }
    try:
        response = requests.post(PAYSTACK_PAYMENT_ENDPOINT, json=json_data, headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"})
        if response and response.status_code == 200 and  response.json()['status']:
            context.update({'successful': True, 'link':response.json()["data"]["authorization_url"]})
    except Exception:
        pass
    return context

def verify(transaction, reference):
    if reference is None:
        return False
    PAYSTACK_VERIFICATION_ENDPOINT = f"https://api.paystack.co/transaction/verify/{reference}"
    try:
        response = requests.get(PAYSTACK_VERIFICATION_ENDPOINT, headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"})
        if response and response.status_code == 200 and response.json()["data"]["status"]=="success" and  response.json()["data"]["amount"]>=transaction.amount*100: # and valid reference
            return True
    except Exception:
        pass
    return False

