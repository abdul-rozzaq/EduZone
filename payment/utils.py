from payment.models import Payment, Promocode
from users.models import User


def can_use_promocode(user: User, promocode: Promocode):
    return not Payment.objects.filter(promocode=promocode, user=user, success=True).exists()
