from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, RegionViewSet, DistrictViewSet, LevelDetailViewSet, LessonDetailViewSet


router = DefaultRouter()

router.register("course", CourseViewSet)
router.register("region", RegionViewSet)
router.register("district", DistrictViewSet)
router.register("levels", LevelDetailViewSet)
router.register("lesson", LessonDetailViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
