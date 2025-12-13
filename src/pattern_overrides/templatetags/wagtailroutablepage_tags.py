from wagtail.contrib.routable_page.templatetags.wagtailroutablepage_tags import register

from pattern_library.monkey_utils import override_tag


override_tag(register, name="routablepageurl", default_html="#")
