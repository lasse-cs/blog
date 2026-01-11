import re

from playwright.sync_api import expect

from wagtail.rich_text import RichText

from article.factories import ArticleIndexPageFactory, ArticlePageFactory
from core.factories import SocialMediaLinksFactory
from home.factories import HomePageFactory


def test_home_page(page, live_site):
    SocialMediaLinksFactory(
        site=live_site,
        links__0="link",
        links__1="link",
    )
    home_page = HomePageFactory(
        title="Home Page Title",
        intro="Welcome to my homepage",
        sidebar__0__text__title="About",
        sidebar__0__text__text=RichText("About this page"),
        sidebar__1__social__title="Connect",
        sidebar__2__tag__title="Topics",
    )
    article_index_page = ArticleIndexPageFactory(
        parent=home_page,
        title="Blog",
        show_in_menus=True,
    )
    article_index_page.save_revision().publish()
    article_1 = ArticlePageFactory(
        parent=article_index_page,
        title="Article 1",
        intro="Article 1 will explain important things",
        tags=["tag1", "tag2", "tag3"],
    )
    article_1.save_revision().publish()
    article_2 = ArticlePageFactory(
        parent=article_index_page,
        title="Article 2",
        intro="Article 2 will probably not explain anything important",
        tags=["tag2", "tag4"],
    )
    article_2.save_revision().publish()
    live_site.root_page = home_page
    live_site.save()
    home_page.save_revision().publish()
    home_page.refresh_from_db()

    # Visiting the home page
    page.goto(f"{home_page.full_url}")
    # The title is visible
    heading = page.get_by_role("heading", level=1)
    expect(heading).to_have_text("Home Page Title")
    # The intro text is there
    intro = page.get_by_text("Welcome to my homepage")
    expect(intro).to_be_visible()

    # The sidebar has an about section
    about_sidebar_section = page.locator(
        "section", has=page.get_by_role("heading", level=2, name="About")
    )
    expect(about_sidebar_section).to_contain_text(re.compile(r"About this page"))

    # The sidebar has a list of social links
    social_sidebar_section = page.locator(
        "section", has=page.get_by_role("heading", level=2, name="Connect")
    )
    social_links = social_sidebar_section.get_by_role("listitem")
    expect(social_links).to_have_count(2)

    # The sidebar has a list of tags
    tag_sidebar_section = page.locator(
        "section", has=page.get_by_role("heading", level=2, name="Topics")
    )
    tag_nav = tag_sidebar_section.get_by_role("navigation", name="Topics")
    tag_nav_links = tag_nav.get_by_role("listitem")
    expect(tag_nav_links).to_have_count(4)

    # Expect the blog page to be linked in the main navigation
    main_navigation = page.get_by_role("navigation", name="Main navigation")
    expect(main_navigation).to_be_attached()
