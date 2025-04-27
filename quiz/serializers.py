from rest_framework import serializers

from .models import UserAnswer, Quiz, QuizQuestion, UserAnswerSheet, QuizAnswer


class QuizAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizAnswer
        exclude = ["is_correct"]


class QuizQuestionSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class UserAnswerSerializer(serializers.ModelSerializer):
    answer_sheet = serializers.PrimaryKeyRelatedField(read_only=True)
    is_correct = serializers.SerializerMethodField()

    class Meta:
        model = UserAnswer
        fields = "__all__"

    def get_is_correct(self, obj):
        return obj.selected_answer.is_correct and obj.question == obj.selected_answer.question


class UserAnswerSheetSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAnswerSheet
        fields = "__all__"

    def create(self, validated_data):
        answers = validated_data.pop("answers")

        answer_sheet = super().create(validated_data)

        for ans in answers:
            UserAnswer.objects.create(**ans, answer_sheet=answer_sheet)

        return answer_sheet
