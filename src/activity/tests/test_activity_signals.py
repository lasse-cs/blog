import pytest

from activity.test.factories import (
    ActivityTrackedModelFactory,
    ActivityTrackedPageFactory,
    ActivityUntrackedPageFactory,
)

from activity.models import Activity, ActivityActions


@pytest.mark.django_db
def test_publishing_page_creates_activity():
    tracked_page = ActivityTrackedPageFactory()
    tracked_page.save_revision().publish()
    activity = Activity.objects.get()
    assert activity.content_object == tracked_page
    assert activity.action == ActivityActions.PUBLISHED


@pytest.mark.django_db
def test_publishing_model_creates_activity():
    tracked_model = ActivityTrackedModelFactory()
    tracked_model.save_revision().publish()
    activity = Activity.objects.get()
    assert activity.content_object == tracked_model
    assert activity.action == ActivityActions.PUBLISHED


@pytest.mark.django_db
def test_publishing_untracked_page_creates_no_activity():
    untracked_page = ActivityUntrackedPageFactory()
    untracked_page.save_revision().publish()
    assert Activity.objects.count() == 0
