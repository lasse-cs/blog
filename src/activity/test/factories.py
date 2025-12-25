from factory.django import DjangoModelFactory
from wagtail_factories import PageFactory

from activity.test.models import (
    ActivityTrackedModel,
    ActivityTrackedPage,
    ActivityUntrackedPage,
)


class ActivityTrackedPageFactory(PageFactory):
    class Meta:
        model = ActivityTrackedPage


class ActivityUntrackedPageFactory(PageFactory):
    class Meta:
        model = ActivityUntrackedPage


class ActivityTrackedModelFactory(DjangoModelFactory):
    class Meta:
        model = ActivityTrackedModel
