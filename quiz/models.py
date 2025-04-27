import uuid

from django.db import models

from core.models import Lesson
from users.models import User


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quiz_questions")
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class QuizQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="quiz-images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz for {self.quiz.name} - {self.text[:50] if self.text else 'Image Question'}"


class QuizAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=256, blank=True, null=True)
    image = models.ImageField(upload_to="quiz-answers/", blank=True, null=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer for {self.question.text[:30] if self.question.text else 'Image Question'} - {'Correct' if self.is_correct else 'Wrong'}"


class UserAnswerSheet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="answer_sheets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_sheets")
    time_spent = models.IntegerField()


class UserAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer_sheet = models.ForeignKey(UserAnswerSheet, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="user_answers")
    selected_answer = models.ForeignKey(QuizAnswer, on_delete=models.CASCADE, related_name="user_selected_answers")

    def __str__(self):
        return f"{self.question.text[:30] if self.question.text else 'Image Question'} - {'Correct' if self.selected_answer.is_correct else 'Wrong'}"
