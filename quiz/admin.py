from django.contrib import admin

from .models import Quiz, QuizQuestion, QuizAnswer, UserAnswer, UserAnswerSheet

from nested_admin import nested


class QuizAnswerInline(nested.NestedTabularInline):
    model = QuizAnswer
    extra = 1


class QuizQuestionInline(nested.NestedTabularInline):
    model = QuizQuestion
    extra = 1
    inlines = [QuizAnswerInline]


@admin.register(Quiz)
class QuizAdmin(nested.NestedModelAdmin):
    list_display = ("id", "lesson", "created_at")
    search_fields = ("lesson__title",)

    inlines = [QuizQuestionInline]


class UserAnswerInline(nested.NestedTabularInline):
    model = UserAnswer
    extra = 1


@admin.register(UserAnswerSheet)
class UserAnswerSheetAdmin(nested.NestedModelAdmin):
    list_display = ("id", "user", "time_spent", "quiz")
    inlines = [UserAnswerInline]
