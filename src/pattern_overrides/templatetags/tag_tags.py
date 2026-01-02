from pattern_library.monkey_utils import override_tag

from core.templatetags.tag_tags import register


override_tag(register, name="tag_list")
