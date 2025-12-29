from wagtail import hooks
from wagtail.snippets.models import register_snippet

from book.views import author_chooser_viewset, AuthorViewSet


register_snippet(AuthorViewSet)


@hooks.register("register_admin_viewset")
def register_author_chooser():
    return author_chooser_viewset
