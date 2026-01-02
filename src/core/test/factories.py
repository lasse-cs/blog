from core.factories import TaggablePageFactory

from core.test.models import AnotherPageWithTags, PageWithTags


class PageWithTagsFactory(TaggablePageFactory):
    class Meta:
        model = PageWithTags


class AnotherPageWithTagsFactory(TaggablePageFactory):
    class Meta:
        model = AnotherPageWithTags
