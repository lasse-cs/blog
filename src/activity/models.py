from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityActions(models.TextChoices):
    PUBLISHED = ("published", "Published")


class Activity(models.Model):
    action = models.CharField(max_length=63, choices=ActivityActions)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created = models.DateTimeField(auto_now_add=True)
