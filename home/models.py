from wagtail.models import Page


class HomePage(Page):
    template = "patterns/pages/home/home_page.html"
