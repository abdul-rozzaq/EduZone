from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Course, Level, Topic, Lesson, QuizQuestion, QuizAnswer, UserAnswer, Leaderboard, FavoriteCourse, LevelPurchase

User = get_user_model()


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        exclude = ["is_correct"]


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    quiz_questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Lesson
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Topic
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()

    class Meta:
        model = Level
        fields = "__all__"

    def get_is_purchased(self, obj):
        return self._get_user_purchased_status(obj)

    def _get_user_purchased_status(self, obj):
        user = self.context.get("request").user

        if not user or not user.is_authenticated:
            return False

        if not hasattr(self, "_user_purchased_cache"):
            self._user_purchased_cache = {}

        if obj.id not in self._user_purchased_cache:
            self._user_purchased_cache[obj.id] = LevelPurchase.objects.filter(user=user, level=obj).exists()

        return self._user_purchased_cache[obj.id]

    def get_topics(self, obj):
        user = self.context.get("request").user
        is_purchased = self._get_user_purchased_status(obj)

        if is_purchased or user.is_staff or user.is_superuser:
            return TopicSerializer(obj.topics.all(), many=True, context={"request": self.context.get("request")}).data

        return []


class CourseSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_favorite(self, obj):
        user = self.context.get("request").user
        return FavoriteCourse.objects.filter(user=user, course=obj).exists()


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = "__all__"


class LeaderboardSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Leaderboard
        fields = "__all__"


class FavoriteCourseSerializer(serializers.Serializer):
    pass
