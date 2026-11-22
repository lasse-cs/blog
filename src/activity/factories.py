from activity.blocks import ActivityBlock
from core.factories import BaseSidebarItemBlockFactory


class ActivityBlockFactory(BaseSidebarItemBlockFactory):
    class Meta:
        model = ActivityBlock
