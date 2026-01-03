from core.models import TaggablePage


class PageWithTags(TaggablePage):
    summary_template = "test/summary.html"


class AnotherPageWithTags(TaggablePage):
    summary_template = "test/summary.html"
