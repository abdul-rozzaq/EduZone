from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, RegionViewSet, DistrictViewSet


router = DefaultRouter()

router.register("course", CourseViewSet)
router.register("region", RegionViewSet)
router.register("district", DistrictViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
