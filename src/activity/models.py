from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.functions import Trunc


class ActivityActions(models.TextChoices):
    PUBLISHED = ("published", "Published")


class ActivityManager(models.Manager):
    def counts_by_day(self):
        return (
            self.annotate(
                activity_date=Trunc(
                    "created", "day", output_field=models.DateTimeField()
                )
            )
            .values("activity_date")
            .annotate(activities=models.Count("id"))
        )


class Activity(models.Model):
    objects = ActivityManager()

    action = models.CharField(max_length=63, choices=ActivityActions)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{ActivityActions(self.action).label}: {self.content_object}"

    def get_activity_description(self):
        return str(self)

    def get_activity_url(self):
        url = getattr(self.content_object, "url", None)
        if not url:
            url = getattr(self.content_object, "get_absolute_url", None)
        return url
