import pytest

from wagtail.rich_text import RichText

from home.factories import HomePageFactory


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("site"),
]


def test_home_page_factory():
    home_page = HomePageFactory(
        sidebar__0__text__title="Title",
        sidebar__0__text__text=RichText("This is the text"),
        sidebar__1="social",
        sidebar__2="text",
    )
    assert len(home_page.sidebar) == 3
    assert home_page.sidebar[0].value["title"] == "Title"
    assert home_page.sidebar[0].value["text"] == RichText("This is the text")
