from rest_framework.routers import DefaultRouter

from .views import QuizViewSet, AnswerSheetViewset

router = DefaultRouter()

router.register("quiz", QuizViewSet)
router.register("answer-sheet", AnswerSheetViewset)

urlpatterns = router.urls + []
