from django.core.mail import send_mail
from raffle.settings import EMAIL_HOST_USER

def send_gmail(subject, message, recepient):
    return send_mail(subject, message, EMAIL_HOST_USER, [recepient],fail_silently = False)