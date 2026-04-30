import pytest
from pytest_django.asserts import assertTemplateUsed
import datetime

from django.urls import reverse

from activity.test.factories import ActivityTrackedPageFactory

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("site"),
]


def test_activity_index_can_be_reached(client):
    url = reverse("activity_index")
    response = client.get(url)
    assert response.status_code == 200


def test_activity_index_template(client):
    url = reverse("activity_index")
    response = client.get(url)
    assertTemplateUsed(response, "patterns/pages/activity/activity_index.html")


def test_activity_index_groups_entries_by_calendar_day(client, root_page, time_machine):
    time_machine.move_to(datetime.datetime(2026, 1, 10, 8, 0, tzinfo=datetime.UTC))
    page_one = ActivityTrackedPageFactory(parent=root_page, title="Tracked page one")
    page_one.save_revision().publish()

    time_machine.shift(datetime.timedelta(hours=3))
    page_two = ActivityTrackedPageFactory(parent=root_page, title="Tracked page two")
    page_two.save_revision().publish()

    time_machine.shift(datetime.timedelta(days=1))
    page_three = ActivityTrackedPageFactory(
        parent=root_page, title="Tracked page three"
    )
    page_three.save_revision().publish()

    url = reverse("activity_index")
    response = client.get(url)

    activities_by_day = response.context["activities_by_day"]
    assert len(activities_by_day) == 2
    assert sorted(len(group) for group in activities_by_day.values()) == [1, 2]
