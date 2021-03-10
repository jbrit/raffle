from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from core.mixins import CustomLoginRequiredMixin

from .models import Transaction

class UserTransactionsView(CustomLoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = "transaction/transactions.html"

    def get_queryset(self):
        return Transaction.objects.filter(made_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_transactions"] = self.get_queryset().filter(is_verified=False)
        context["verified_transactions"] = self.get_queryset().filter(is_verified=True)
        return context


class UserTransactionDetailView(CustomLoginRequiredMixin, DetailView):
    model = Transaction
    pk_url_kwarg = "id"
    context_object_name = 'transaction'
    template_name = "transaction/transaction_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        link = self.get_object().get_payment_data(self.request)
        context["transaction_link"] = link if len(link) else "#"
        return context


class TransactionCreationView(CustomLoginRequiredMixin, CreateView):
    model = Transaction
    success_url = reverse_lazy("transactions")
    template_name = "transaction/transaction_create.html"
    fields = ['amount']

    def form_valid(self, form):
        form.instance.made_by = self.request.user
        return super().form_valid(form)
    

# TODO: login_required decorator
def transaction_verification_view(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    tx_id = request.GET.get("transaction_id",0)
    transaction.verify(tx_id)
    return redirect('transaction_detail', id=transaction.eight_digit_id)
