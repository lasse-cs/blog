from wagtail.blocks import StreamBlock

from activity.blocks import ActivityBlock
from core.blocks import SocialBlock, TagBlock, TitledTextBlock
from search.blocks import SearchBlock


class HomePageSidebarBlock(StreamBlock):
    text = TitledTextBlock()
    social = SocialBlock()
    activity = ActivityBlock()
    tag = TagBlock()
    search = SearchBlock()

    class Meta:
        template = "patterns/components/sidebar/sidebar.html"
        block_counts = {
            "social": {"max_num": 1},
            "activity": {"max_num": 1},
            "tag": {"max_num": 1},
            "search": {"max_num": 1},
        }
