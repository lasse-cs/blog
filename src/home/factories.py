from wagtail_factories import PageFactory, StreamFieldFactory

from core.factories import SidebarBlockFactory
from home.models import HomePage


class HomePageFactory(PageFactory):
    sidebar = StreamFieldFactory(SidebarBlockFactory)

    class Meta:
        model = HomePage
