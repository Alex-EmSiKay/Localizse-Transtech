from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import related
from django.db.models.fields.reverse_related import ManyToManyRel
from django.utils import timezone


# Create your models here.


class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    primary = models.ManyToManyField(Language, related_name="primary_users")
    secondary = models.ManyToManyField(
        Language, blank=True, related_name="secondary_users"
    )
    # determines the languages displayed in the work view
    active_pri = models.ForeignKey(
        Language, null=True, on_delete=SET_NULL, related_name="primary_users_active"
    )
    # ditto
    active_sec = models.ForeignKey(
        Language, null=True, on_delete=SET_NULL, related_name="secondary_users_active"
    )
    locked = models.DateTimeField(blank=True, null=True)
    # a key to make sure users can't upgrade randomly
    offer = models.UUIDField(blank=True, null=True)


class TechContent(models.Model):
    pass


class TechContentVersion(models.Model):
    V_TYPES = (
        ("OR", "Original"),
        ("TR", "Translation"),
    )
    STATUSES = (
        ("C", "Created"),
        ("R", "Reviewed"),
        ("A", "Audited"),
        ("O", "Original version"),
    )
    content_id = models.ForeignKey(
        "TechContent", on_delete=models.CASCADE, related_name="versions"
    )
    language = models.ForeignKey(Language, on_delete=CASCADE)
    content = models.TextField()
    version_type = models.CharField(max_length=2, choices=V_TYPES)
    status = models.CharField(max_length=1, choices=STATUSES)

    def __str__(self):
        return f"TechContent {self.content_id.pk} - {self.language.name}"


class Item(models.Model):
    WORK_TYPES = (
        ("RE", "Review"),
        ("AU", "Audit"),
    )
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="items")
    content = models.ForeignKey(
        TechContentVersion, null=True, on_delete=SET_NULL, related_name="reviews"
    )
    initial = models.TextField()  # these are used to
    final = models.TextField()  # check accuracy
    work_type = models.CharField(max_length=2, choices=WORK_TYPES)
    done = models.DateTimeField(default=timezone.now)


class Report(models.Model):
    reporter = models.ForeignKey(User, on_delete=CASCADE, related_name="reports")
    description = models.TextField()
    version = models.ForeignKey(
        TechContentVersion, on_delete=CASCADE, related_name="reports"
    )
    reported_at = models.DateTimeField(default=timezone.now)


class Message(models.Model):
    recipient = models.ForeignKey(
        User, blank=True, null=True, on_delete=CASCADE, related_name="messages"
    )
    subject = models.CharField(max_length=64)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
