from core.blocks import BaseSidebarItemBlock


class SearchBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/search_block.html"
        icon = "search"
