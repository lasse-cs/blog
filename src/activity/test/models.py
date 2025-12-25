from django.db import models

from wagtail.models import DraftStateMixin, RevisionMixin, Page


class ActivityTrackedPage(Page):
    track_activity = True


class ActivityTrackedModel(DraftStateMixin, RevisionMixin, models.Model):
    track_activity = True


class ActivityUntrackedPage(Page):
    track_activity = False
