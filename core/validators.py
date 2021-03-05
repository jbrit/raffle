from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_room(room: str) -> None:
    if room.lower()[0] not in "abcdefg" or len(room) != 4 or not room[1:].isnumeric():
        raise ValidationError(
            _('%(value)s is not a valid room number'),
            params={'value': room},
        )