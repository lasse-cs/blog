from core.factories import BaseSidebarItemBlockFactory

from search.blocks import SearchBlock


class SearchBlockFactory(BaseSidebarItemBlockFactory):
    class Meta:
        model = SearchBlock
