from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Quiz, UserAnswerSheet
from .serializers import QuizSerializer, UserAnswerSheetSerializer


class QuizViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    @action(["POST"], detail=True, serializer_class=UserAnswerSheetSerializer)
    def solve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print(serializer.data)

        return Response(serializer.data)


class AnswerSheetViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserAnswerSheetSerializer
    queryset = UserAnswerSheet.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)
