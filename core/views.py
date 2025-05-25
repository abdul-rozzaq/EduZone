from django.db.models import Count
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import render

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Course, FavoriteCourse, Lesson, Level, Topic, LevelPurchase
from .serializers import CourseSerializer, FavoriteCourseSerializer, LessonSerializer, LevelSerializer, TopicSerializer
from .filters import CourseFilter, DistrictFilter

from users.models import Region, District
from users.serializers import RegionSerializer, DistrictSerializer


class CourseViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter

    @swagger_auto_schema(manual_parameters=[openapi.Parameter("purchased", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="Filter by purchased")])
    @action(["GET"], detail=False)
    def popular(self, request, *args, **kwargs):
        purchased = request.GET.get("purchased", "")
        courses = self.get_queryset()

        if purchased.lower() == "true":
            courses = courses.filter(purchases__user=request.user)
        elif purchased.lower() == "false":
            courses = courses.exclude(purchases__user=request.user)

        top_courses = courses.annotate(purchase_count=Count("purchases")).order_by("-purchase_count")[:2]
        serializer = self.get_serializer(top_courses, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(methods=["POST", "DELETE"], request_body=FavoriteCourseSerializer)
    @action(["POST", "DELETE"], detail=True)
    def favorite(self, request, *args, **kwargs):
        user = request.user
        course = self.get_object()

        if request.method == "POST":
            _, created = FavoriteCourse.objects.get_or_create(user=user, course=course)

            return Response({"message": "Kurs muvaffaqiyatli qo'shildi" if created else "Kurs allaqachon qo'shilgan"}, status=201 if created else 400)

        deleted, _ = FavoriteCourse.objects.filter(user=user, course=course).delete()

        return Response({"message": "Kurs muvaffaqiyatli olib tashlandi" if deleted else "Kurs saqlanganlarga qo'shilmagan"}, status=200 if deleted else 400)

    @swagger_auto_schema(manual_parameters=[openapi.Parameter("is_favorited", in_=openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN, description="Filter by favorite")])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RegionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DistrictViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filterset_class = DistrictFilter
    search_fields = ["name"]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="region_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Filter by region ID"),
            openapi.Parameter(name="search", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Search by district name"),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LevelDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.all()


class LessonDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class TopicViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        level_purchase = LevelPurchase.objects.filter(user=user, level=obj.level).exists()

        if level_purchase or user.is_staff or user.is_superuser:
            return obj
        

        raise PermissionDenied()


def home_page(request):
    return render(request, 'index.html', {})