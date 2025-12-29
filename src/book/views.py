from wagtail.admin.panels import FieldPanel
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.snippets.views.snippets import SnippetViewSet

from book.models import Author


class AuthorViewSet(SnippetViewSet):
    model = Author

    panels = [
        FieldPanel("name"),
    ]


class AuthorChooserViewSet(ChooserViewSet):
    model = Author

    icon = "user"
    choose_one_text = "Select an author"
    choose_another_text = "Select another author"
    edit_item_text = "Edit this author"
    form_fields = ["name"]


author_chooser_viewset = AuthorChooserViewSet("author_chooser")
