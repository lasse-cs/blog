import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.usefixtures("site")
def test_robots_txt_get(client):
    response = client.get(reverse("robots_txt"))
    assert response.status_code == 200
    assert "text/plain" in response.headers["Content-Type"]
    assertTemplateUsed(response, "non_patterns/robots.txt")


@pytest.mark.django_db
@pytest.mark.usefixtures("site")
def test_robots_txt_contains_sitemap_url(client):
    response = client.get(reverse("robots_txt"))
    assert reverse("sitemap") in response.content.decode()


@pytest.mark.django_db
@pytest.mark.usefixtures("site")
def test_robots_txt_post_not_allowed(client):
    response = client.post(reverse("robots_txt"))
    assert response.status_code == 405
