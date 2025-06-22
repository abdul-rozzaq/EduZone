from rest_framework import serializers

from core.models import Level
from .models import Payment, Promocode


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        exclude = ["transaction_id"]


class CreatePaymentSerializer(serializers.Serializer):
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

    card_number = serializers.CharField(max_length=16)
    card_expiry = serializers.CharField(max_length=5)

    promocode = serializers.PrimaryKeyRelatedField(queryset=Promocode.objects.all(), required=False, allow_null=True)


class VerifyPaymentSerializer(serializers.Serializer):
    sms_code = serializers.CharField(max_length=6)


class CheckPromocodeSerializer(serializers.Serializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    code = serializers.CharField()


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = "__all__"
