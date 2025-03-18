from django.contrib.auth import views
from django.urls import path, include

from .views import logout_page
from .routers import router


urlpatterns = [
    path("logout/", logout_page, name="logout"),
    path("", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(router.urls)),
]
