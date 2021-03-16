from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_transaction_amount(amount) -> None:
    if amount < 100 or amount % 100 != 0:
        raise ValidationError(
            _('Amount must be a multiple of 100'),
            params={'value': amount},
        )
    if amount < 500:
        raise ValidationError(
            _('Amount must be at least 500'),
            params={'value': amount},
        )