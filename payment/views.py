from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from payment.models import Payment
from payment.serializers import CreatePaymentSerializer, VerifyPaymentSerializer
from payment.payment_utils import create_card_token, verify_token, payment_with_token

from click_up.views import ClickWebhook


class PaymentViewSet(GenericViewSet):
    queryset = Payment.objects.all()

    def get_serializer_class(self):
        if self.action == "create_payment":
            return CreatePaymentSerializer

        elif self.action == "verify_payment":
            return VerifyPaymentSerializer

        return super().get_serializer_class()

    @action(["POST"], detail=False, url_path="create-payment")
    def create_payment(self, request, *args, **kwargs):
        """
        To'lov amalga oshirish
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_number = serializer.validated_data.get("card_number")
        card_expiry = serializer.validated_data.get("card_expiry")
        level = serializer.validated_data.get("level")

        # status_code, response_body = 200, {"error_code": 0, "card_token": "1f14684a-7480-49c1-b635-2ef25f46f01d"}
        status_code, response_body = create_card_token(card_number, card_expiry)

        card_token = response_body.get("card_token")
        error_code = response_body.get("error_code")

        if status_code != 200 or error_code != 0:
            return Response({"error": "Token yaratishda xatolik"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            level=level,
            amount=level.price,
            token=card_token,
        )

        return Response({"message": "Token muvaffaqiyatli yaratildi", "payment_id": payment.id}, status=201)

    @action(["POST"], detail=True, url_path="verify-payment")
    def verify_payment(self, request, *args, **kwargs):
        """
        To'lovni tasdiqlash
        """
        payment: Payment = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sms_code = serializer.validated_data["sms_code"]

        status_code, response = verify_token(payment.token, sms_code)

        error_code = response.get("error_code")

        if status_code != 200 or error_code != 0:
            return Response({"error": "Tokenni tasdiqlashda xatolik"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            status_code, response = payment_with_token(payment.token, payment.level.price, payment_id=str(payment.pk))
        except Exception as e:
            return Response({"error": "To'lovni amalga oshirishda xatolik"}, status=status.HTTP_400_BAD_REQUEST)

        if status_code != 200 or error_code != 0:
            return Response({"error": "To'lovni amalga oshirishda xatolik"}, status=status.HTTP_400_BAD_REQUEST)

        payment.confirm()
        payment.create_purchase()

        return Response({"message": "To'lov tasdiqlandi"}, status=200)


class ClickWebhookAPIView(ClickWebhook):
    def successfully_payment(self, params):
        """
        successfully payment method process you can ovveride it
        """
        print(f"payment successful params: {params}")

    def cancelled_payment(self, params):
        """
        cancelled payment method process you can ovveride it
        """
        print(f"payment cancelled params: {params}")
