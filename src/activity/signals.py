from django.dispatch import receiver
from wagtail.signals import published

from activity.models import Activity, ActivityActions


@receiver(published, dispatch_uid="activity_on_publish")
def add_activity_for_published(sender, **kwargs):
    if not getattr(sender, "track_activity", False):
        return
    Activity.objects.create(
        action=ActivityActions.PUBLISHED, content_object=kwargs["instance"]
    )
