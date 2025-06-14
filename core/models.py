import uuid

from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_video_file


User = get_user_model()


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to="course-images/")
    intro = models.FileField(validators=[validate_video_file], upload_to="course-intro-videos/")
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Level(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField("Level Image", upload_to="level-images/")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="levels")
    name = models.CharField(max_length=256)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.level.name} - {self.name}"


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=256)
    video_url = models.URLField()

    def __str__(self):
        return f"{self.topic.name} - {self.title}"


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="leaderboard")
    total_score = models.IntegerField(default=0)
    total_time_spent = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Score: {self.total_score}"


class FavoriteCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class LevelPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchased_levels")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="purchases")
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.level.name}"
