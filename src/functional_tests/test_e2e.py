from playwright.sync_api import expect

from home.factories import HomePageFactory


def test_home_page(page, live_site):
    home_page = HomePageFactory(
        title="Home Page Title",
    )
    live_site.root_page = home_page
    live_site.save()
    home_page.refresh_from_db()
    page.goto(f"{home_page.full_url}")

    heading = page.get_by_role("heading", level=1)
    expect(heading).to_have_text("Home Page Title")
