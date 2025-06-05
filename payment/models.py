import uuid

from django.db import models

from core.models import Level, LevelPurchase
from users.models import User

from django.utils import timezone


class Promocode(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    code = models.CharField(max_length=128, unique=True, db_index=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Promo kod hali ham amal qilayotganini qaytaradi"""
        if self.expires_at:
            return timezone.now() < self.expires_at
        return True

    def __str__(self):
        return self.code


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    promocode = models.ForeignKey(Promocode, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)

    success = models.BooleanField(default=False)

    token = models.CharField(max_length=128)
    transaction_id = models.CharField(max_length=128, unique=True, null=True, blank=True)

    def __str__(self):
        return f"Payment(user={self.user}, course={self.level}, amount={self.amount}, date={self.date}, success={self.success})"

    def is_successful(self):
        """To'lov muvaffaqiyatli amalga oshirilganmi?"""
        return self.success

    def confirm(self):
        self.success = True
        self.transaction_id = uuid.uuid4()

        self.save()

    def create_purchase(self):
        return LevelPurchase.objects.create(user=self.user, level=self.level)
