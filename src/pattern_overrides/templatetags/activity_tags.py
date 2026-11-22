from pattern_library.monkey_utils import override_tag

from activity.templatetags.activity_tags import register

override_tag(register, name="recent_activity")
