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

    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop("exclude_fields", None)

        super().__init__(*args, **kwargs)

        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field)


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class UserAnswerSerializer(serializers.ModelSerializer):
    answer_sheet = serializers.PrimaryKeyRelatedField(read_only=True)
    is_correct = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserAnswer
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["question"] = QuizQuestionSerializer(instance.question, exclude_fields=["answers"], context={"request": self.context.get("request")}).data
        data["selected_answer"] = QuizAnswerSerializer(instance.selected_answer, context={"request": self.context.get("request")}).data

        return data


class UserAnswerSheetSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quiz = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserAnswerSheet
        fields = "__all__"

    def create(self, validated_data):
        answers = validated_data.pop("answers")

        answer_sheet = super().create(validated_data)

        answers = [UserAnswer(**ans, answer_sheet=answer_sheet) for ans in answers]

        UserAnswer.objects.bulk_create(answers)

        return answer_sheet

    def to_representation(self, instance):
        data = super().to_representation(instance)

        answers = instance.answers.all()

        total_questions = instance.quiz.questions.count()
        
        for i in answers:
            print(i.is_correct)
        
        correct_answers = instance.answers.filter(is_correct=True).count()
        wrong_answers = instance.answers.filter(is_correct=False).count()

        # print(correct_answers, wrong_answers)
        # print(instance.answers.all().filter(is_correct=True))

        data["total_questions"] = total_questions
        data["correct_answers"] = correct_answers
        data["wrong_answers"] = wrong_answers
        data["xp"] = instance.quiz.xp * correct_answers

        return data
