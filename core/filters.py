from django_filters import rest_framework as filters
from users.models import District
from .models import Course


class DistrictFilter(filters.FilterSet):
    class Meta:
        model = District
        fields = ["region_id"]


class CourseFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method="filter_favorited")

    class Meta:
        model = Course
        fields = []

    def filter_favorited(self, queryset, name, value):
        user = self.request.user

        if value:
            return queryset.filter(favorited_by__user=user)

        return queryset
