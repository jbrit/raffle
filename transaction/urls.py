from django.urls import  path, re_path
from django.conf import settings

from .views import  UserTransactionsView, transaction_verification_view, UserTransactionDetailView, TransactionCreationView

urlpatterns = [
    path('transactions/', UserTransactionsView.as_view(), name="transactions"),
    path('transactions/create/', TransactionCreationView.as_view(), name="transaction_create"),
    ] 

if settings.FLUTTERWAVE_PRODUCTION:
    urlpatterns += [
        re_path(r'transactions/rftx-(?P<id>[0-9]{8})/$', UserTransactionDetailView.as_view(), name="transaction_detail"),
        re_path(r'transactions/rftx-(?P<id>[0-9]{8})/verify/$', transaction_verification_view, name="transaction_verify")
    ]
else:
    urlpatterns += [
        re_path(r'transactions/rftx-test-(?P<id>[0-9]{8})/$', UserTransactionDetailView.as_view(), name="transaction_detail"),
        re_path(r'transactions/rftx-test-(?P<id>[0-9]{8})/verify/$', transaction_verification_view, name="transaction_verify")
    ]
