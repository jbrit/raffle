import requests
from django.conf import settings

FLUTTER_PAYMENT_ENDPOINT = "https://api.flutterwave.com/v3/payments"

def get_payment_url(transaction, user, redirect_url):
    json_data = {
        "tx_ref": f"{transaction.tx_ref}",
        "amount": f"{transaction.amount}",
        "currency":"NGN",
        "redirect_url": f"{redirect_url}",
        "payment_options":"card",
        "meta":{
            "consumer_id": f"{user.id}",
        },
        "customer":{
            "email": f"{user.email}",
            "name": f"{user.profile.get_full_name()}"
        },
        "customizations":{
            "title":"Raffle Wallet Payments", # TODO: Change name later
            "description": f"Payment of N{transaction.amount} into wallet",
            # "logo":"https://assets.piedpiper.com/logo.png" TODO: Logo link
        }
    }
    context = {'successful': False, 'link': '' }
    try:
        response = requests.post(FLUTTER_PAYMENT_ENDPOINT, json=json_data, headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"})
        if response and response.status_code == 200 and  response.json()['status'] == 'success':
            context.update({'successful': True, 'link':response.json()["data"]["link"]})
    except Exception:
        pass
    return context

def verify(transaction, tx_id):
    FLUTTER_VERIFICATION_ENDPOINT = f"https://api.flutterwave.com/v3/transactions/{tx_id}/verify"
    try:
        response = requests.get(FLUTTER_VERIFICATION_ENDPOINT, headers = {"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"})
        if response and response.status_code == 200 and response.json()["data"]["status"]=="successful" and  response.json()["data"]["amount"]>=transaction.amount and response.json()["data"]["tx_ref"]==transaction.tx_ref:
            return True
    except Exception:
        pass
    return False

