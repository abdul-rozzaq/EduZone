from django.db import models
from .validators import validate_video_file
import uuid


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to="course-images/")
    intro = models.FileField(validators=[validate_video_file], upload_to="course-intro-videos/")
    price = models.IntegerField()

    def __str__(self):
        return self.name
