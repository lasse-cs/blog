from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.models import Page, Orderable
from wagtail.search import index

from core.models import FeedItemMixin, FeedMixin


Image = get_image_model()


class Author(models.Model):
    name = models.CharField(max_length=255, help_text="The full name of the author.")

    def __str__(self):
        return self.name


class BookAuthor(Orderable, models.Model):
    book = ParentalKey(
        "book.BookPage", on_delete=models.CASCADE, related_name="book_authors"
    )
    author = models.ForeignKey(
        "book.Author", on_delete=models.CASCADE, related_name="books_authored"
    )

    panels = [
        FieldPanel("author"),
    ]

    def __str__(self):
        return f"{self.author.name} <-> {self.book.title}"


class BookIndexPage(FeedMixin, Page):
    intro = RichTextField(
        help_text="Intro text for the Book Index Page.",
        default="Book Index Page intro content.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    per_page = 12
    subpage_types = ["book.BookPage"]
    template = "patterns/pages/book/book_index_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        page_number = request.GET.get("page", 1)
        page, page_range = self.get_paginated_feed_items(page_number)
        context["pagination_page"] = page
        context["page_range"] = page_range
        return context


class BookPage(FeedItemMixin, Page):
    blurb = RichTextField(
        help_text="The blurb for the book.",
        default="Book blurb",
    )
    cover_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The cover image for the model",
    )
    progress = models.PositiveSmallIntegerField(
        default=0,
        help_text="The progress through the book, as a percentage",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    content_panels = content_panels = (
        Page.content_panels
        + FeedItemMixin.panels
        + [
            InlinePanel("book_authors"),
            FieldPanel("cover_image"),
            FieldPanel("blurb"),
            FieldPanel("progress"),
        ]
    )

    search_fields = (
        Page.search_fields
        + FeedItemMixin.search_fields
        + [
            index.SearchField("blurb"),
        ]
    )

    parent_page_types = ["book.BookIndexPage"]
    subpage_types = []

    summary_template = "patterns/components/book/book_summary.html"
    template = "patterns/pages/book/book_page.html"
