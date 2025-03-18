from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CourseViewSet


router = DefaultRouter()

router.register("course", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
