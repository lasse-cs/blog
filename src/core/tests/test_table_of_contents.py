import pytest

from core.blocks import HeadingLevelChoices
from core.models import TableOfContentsItem

from core.test.factories import (
    PageWithTableOfContentsFactory,
    PageWithTableOfContentsH3Factory,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("site"),
]


def test_table_of_contents_with_no_blocks():
    toc_page = PageWithTableOfContentsFactory()
    assert toc_page.table_of_contents == []


def test_table_of_contents():
    toc_page = PageWithTableOfContentsFactory(
        body__0__heading__level=HeadingLevelChoices.H2,
        body__0__heading__heading="Heading",
        body__1__heading__level=HeadingLevelChoices.H3,
        body__1__heading__heading="Heading2",
        body__2__heading_list__0__level=HeadingLevelChoices.H3,
        body__2__heading_list__0__heading="Heading3",
        body__3__heading_struct__heading__level=HeadingLevelChoices.H4,
        body__3__heading_struct__heading__heading="Heading4",
        body__4__heading_stream__0__heading__level=HeadingLevelChoices.H3,
        body__4__heading_stream__0__heading__heading="Heading5",
    )
    assert toc_page.table_of_contents == [
        TableOfContentsItem(
            level=HeadingLevelChoices.H2,
            heading="Heading",
            children=[
                TableOfContentsItem(
                    level=HeadingLevelChoices.H3,
                    heading="Heading2",
                ),
                TableOfContentsItem(
                    level=HeadingLevelChoices.H3,
                    heading="Heading3",
                    children=[
                        TableOfContentsItem(
                            level=HeadingLevelChoices.H4,
                            heading="Heading4",
                        )
                    ],
                ),
                TableOfContentsItem(
                    level=HeadingLevelChoices.H3,
                    heading="Heading5",
                ),
            ],
        )
    ]


def test_table_of_contents_with_h4_without_h3():
    toc_page = PageWithTableOfContentsFactory(
        body__0__heading__level=HeadingLevelChoices.H2,
        body__0__heading__heading="Heading",
        body__1__heading__level=HeadingLevelChoices.H4,
        body__1__heading__heading="Heading4",
    )

    assert toc_page.table_of_contents == [
        TableOfContentsItem(
            level=HeadingLevelChoices.H2,
            heading="Heading",
            children=[
                TableOfContentsItem(
                    level=HeadingLevelChoices.H4,
                    heading="Heading4",
                )
            ],
        )
    ]


def test_table_of_contents_h3_only_model_excludes_h4():
    toc_page = PageWithTableOfContentsH3Factory(
        body__0__heading__level=HeadingLevelChoices.H2,
        body__0__heading__heading="Heading",
        body__1__heading__level=HeadingLevelChoices.H3,
        body__1__heading__heading="Heading2",
        body__2__heading__level=HeadingLevelChoices.H4,
        body__2__heading__heading="Heading3",
    )

    assert toc_page.table_of_contents == [
        TableOfContentsItem(
            level=HeadingLevelChoices.H2,
            heading="Heading",
            children=[
                TableOfContentsItem(
                    level=HeadingLevelChoices.H3,
                    heading="Heading2",
                )
            ],
        )
    ]
