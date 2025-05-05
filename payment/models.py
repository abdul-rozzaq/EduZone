import uuid

from django.db import models

from core.models import Level, LevelPurchase
from users.models import User


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
