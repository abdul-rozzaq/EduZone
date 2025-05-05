from rest_framework import serializers

from core.models import Course, Level
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = "__all__"


class CreatePaymentSerializer(serializers.Serializer):
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

    card_number = serializers.CharField(max_length=16)
    card_expiry = serializers.CharField(max_length=5)


class VerifyPaymentSerializer(serializers.Serializer):
    sms_code = serializers.CharField(max_length=6)
