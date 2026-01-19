import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

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
