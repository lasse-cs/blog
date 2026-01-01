import datetime
import pytest

from activity.models import Activity
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
    actual = {a["activity_day"]: a["activities"] for a in actual_list}
    assert actual == expected


@pytest.mark.django_db
def test_activity_counts_with_filter(root_page, time_machine):
    time_machine.move_to(datetime.datetime(2000, 1, 1, tzinfo=datetime.UTC))
    page = ActivityTrackedPageFactory(parent=root_page)
    page.save_revision().publish()
    time_machine.shift(datetime.timedelta(days=8))
    page.save_revision().publish()

    last_week = datetime.datetime.now() - datetime.timedelta(days=8)

    expected = {
        datetime.datetime(2000, 1, 9, tzinfo=datetime.UTC): 1,
    }
    actual_list = Activity.objects.counts_by_day().filter(created__gt=last_week)
    actual = {a["activity_day"]: a["activities"] for a in actual_list}
    assert actual == expected
