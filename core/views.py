from rest_framework import mixins, viewsets
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
