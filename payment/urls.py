from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet


router = DefaultRouter()

router.register(r"payment", PaymentViewSet, basename="payment")


urlpatterns = router.urls + []
