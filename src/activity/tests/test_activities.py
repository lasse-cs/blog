import datetime
import pytest

from activity.models import Activity
from activity.templatetags.activity_tags import recent_activity
from activity.test.factories import ActivityTrackedPageFactory


@pytest.mark.django_db
def test_activity_counts(root_page, time_machine):
    time_machine.move_to(datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC))
    page = ActivityTrackedPageFactory(parent=root_page)
    page.save_revision().publish()
    time_machine.shift(datetime.timedelta(days=2))
    page.save_revision().publish()
    page.save_revision().publish()
    time_machine.shift(datetime.timedelta(days=4))
    page.save_revision().publish()

    expected = {
        datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC): 1,
        datetime.datetime(2000, 1, 3, tzinfo=datetime.UTC): 2,
        datetime.datetime(2000, 1, 7, tzinfo=datetime.UTC): 1,
    }

    actual_list = Activity.objects.counts_by_day()
    actual = {a["activity_date"]: a["activities"] for a in actual_list}
    assert actual == expected


@pytest.mark.django_db
def test_recent_activities(root_page, time_machine):
    time_machine.move_to(datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC))
    page = ActivityTrackedPageFactory(parent=root_page)
    page.save_revision().publish()
    time_machine.shift(datetime.timedelta(days=8))
    page.save_revision().publish()

    expected = {
        datetime.date(2000, 1, 9): 1,
        datetime.date(2000, 1, 8): 0,
        datetime.date(2000, 1, 7): 0,
        datetime.date(2000, 1, 6): 0,
        datetime.date(2000, 1, 5): 0,
        datetime.date(2000, 1, 4): 0,
        datetime.date(2000, 1, 3): 0,
    }
    actual_list = recent_activity()
    actual = {a["activity_date"]: a["activities"] for a in actual_list}
    assert actual == expected
