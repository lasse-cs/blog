from core.factories import BaseSidebarItemBlockFactory

from activity.blocks import ActivityBlock


class ActivityBlockFactory(BaseSidebarItemBlockFactory):
    class Meta:
        model = ActivityBlock
