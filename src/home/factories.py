import factory
from wagtail_factories import PageFactory, StreamBlockFactory, StreamFieldFactory

from activity.factories import ActivityBlockFactory
from core.factories import SocialBlockFactory, TagBlockFactory, TitledTextBlockFactory
from home.blocks import HomePageSidebarBlock
from home.models import HomePage
from search.factories import SearchBlockFactory


class HomePageSidebarBlockFactory(StreamBlockFactory):
    text = factory.SubFactory(TitledTextBlockFactory)
    social = factory.SubFactory(SocialBlockFactory)
    activity = factory.SubFactory(ActivityBlockFactory)
    tag = factory.SubFactory(TagBlockFactory)
    search = factory.SubFactory(SearchBlockFactory)

    class Meta:
        model = HomePageSidebarBlock


class HomePageFactory(PageFactory):
    sidebar = StreamFieldFactory(HomePageSidebarBlockFactory)

    class Meta:
        model = HomePage
