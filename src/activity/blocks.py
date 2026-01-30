from core.blocks import BaseSidebarItemBlock


class ActivityBlock(BaseSidebarItemBlock):
    class Meta:
        template = "patterns/components/sidebar/blocks/activity_block.html"
        icon = "time"
