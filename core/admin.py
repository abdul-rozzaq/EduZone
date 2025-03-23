from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Level, Topic, Lesson, QuizQuestion, QuizAnswer, LevelPurchase


class LevelInline(admin.TabularInline):
    model = Level
    extra = 1


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 2


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview")
    search_fields = ("name",)
    inlines = [LevelInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.image.url)
        return "-"

    image_preview.short_description = "Image"


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "price")
    search_fields = ("name", "course__name")
    list_filter = ("course", "price")
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "level")
    search_fields = ("name", "level__name")
    list_filter = ("level",)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "topic")
    search_fields = ("title", "topic__name")
    list_filter = ("topic",)

    # def video_preview(self, obj):
    #     if obj.video:
    #         return format_html('<video width="100" controls><source src="{}" type="video/mp4"></video>', obj.video.url)
    #     return "-"
    # video_preview.short_description = "Video"


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "lesson", "created_at", "image_preview")
    search_fields = ("text", "lesson__title")
    list_filter = ("created_at", "lesson")
    inlines = [QuizAnswerInline]

    def short_text(self, obj):
        return obj.text[:50] if obj.text else "Image Question"

    short_text.short_description = "Question"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.image.url)
        return "-"

    image_preview.short_description = "Image"


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ("short_text", "question", "is_correct", "image_preview")
    search_fields = ("text", "question__text")
    list_filter = ("is_correct",)

    def short_text(self, obj):
        return obj.text[:30] if obj.text else "Image Answer"

    short_text.short_description = "Answer"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.image.url)
        return "-"

    image_preview.short_description = "Image"


@admin.register(LevelPurchase)
class LevelPurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "purchased_at")
    list_filter = ("user", "level")


# @admin.register(UserAnswer)
# class UserAnswerAdmin(admin.ModelAdmin):
#     list_display = ("user", "question", "selected_answer", "is_correct", "time_spent")
#     search_fields = ("user__username", "question__text")
#     list_filter = ("time_spent",)

#     def is_correct(self, obj):
#         return obj.selected_answer.is_correct

#     is_correct.boolean = True
#     is_correct.short_description = "Correct"


# @admin.register(Leaderboard)
# class LeaderboardAdmin(admin.ModelAdmin):
#     list_display = ("user", "total_score", "total_time_spent")
#     search_fields = ("user__username",)
#     list_filter = ("total_score",)


# @admin.register(FavoriteCourse)
# class FavoriteCourseAdmin(admin.ModelAdmin):
#     list_display = ("user", "course", "added_at")
#     search_fields = ("user__username", "course__name")
#     list_filter = ("added_at",)
