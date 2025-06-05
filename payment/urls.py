from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ClickWebhookAPIView, PaymentViewSet


router = DefaultRouter()

router.register(r"payment", PaymentViewSet, basename="payment")


urlpatterns = router.urls + [
    path("payment/click/update/", ClickWebhookAPIView.as_view()),
]
