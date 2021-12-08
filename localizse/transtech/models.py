from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class TechContent(models.Model):
    pass


class TechContentVersion(models.Model):
    LANGS = (
        ("en", "English"),
        ("fr", "French"),
        ("pt", "Portuguese"),
        ("zh", "Chinese"),
    )
    V_TYPES = (
        ("OR", "Original"),
        ("TR", "Translation"),
    )
    STATUSES = (
        ("C", "Created"),
        ("R", "Reviewed"),
        ("O", "Original version"),
    )
    content_id = models.ForeignKey(
        "TechContent", on_delete=models.CASCADE, related_name="versions"
    )
    language = models.CharField(max_length=2, choices=LANGS)
    content = models.TextField()
    version_type = models.CharField(max_length=2, choices=V_TYPES)
    status = models.CharField(max_length=1, choices=STATUSES)
