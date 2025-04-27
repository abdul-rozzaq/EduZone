from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Level, Topic, Lesson, LevelPurchase


class LevelInline(admin.TabularInline):
    model = Level
    extra = 1


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


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


# @admin.register(Lesson)
# class LessonAdmin(admin.ModelAdmin):
#     list_display = ("title", "topic")
#     search_fields = ("title", "topic__name")
#     list_filter = ("topic",)

#     def video_preview(self, obj):
#         if obj.video:
#             return format_html('<video width="100" controls><source src="{}" type="video/mp4"></video>', obj.video.url)
#         return "-"
#     video_preview.short_description = "Video"


@admin.register(LevelPurchase)
class LevelPurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "purchased_at")
    list_filter = ("user", "level")
