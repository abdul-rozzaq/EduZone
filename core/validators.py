from django.core.exceptions import ValidationError


def validate_video_file(value):
    allowed_extensions = ["mp4", "avi", "mov", "mkv", "flv", "wmv"]
    if not value.name.split(".")[-1].lower() in allowed_extensions:
        raise ValidationError("Faqat video fayllar yuklanishi mumkin! (Ruxsat etilgan formatlar: mp4, avi, mov, mkv, flv, wmv)")
