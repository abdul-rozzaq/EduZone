from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API documentation for my project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


api_urlpatterns = [
    path("", include("payment.urls")),
    path("", include("core.api_urls")),
    path("", include("quiz.api_urls")),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("api/v1/", include(api_urlpatterns)),
    path("api/v1/auth/", include("users.urls"), name="auth"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
