from rest_framework import mixins, viewsets

from .models import Course
from .serializers import CourseSerializer

from users.models import Region, District
from users.serializers import RegionSerializer, DistrictSerializer


class CourseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class RegionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    filterset_fields = ["region_id"]
    search_fields = ["name"]
