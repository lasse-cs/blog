import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_404_view(client):
    response = client.get("/this-view-should-not-be-found/")
    assert response.status_code == 404
    assertTemplateUsed("patterns/pages/error/404.html")
