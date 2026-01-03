from django.urls import path

from core.views import tagged_pages

urlpatterns = [
    path("tags/<slug:tag_slug>/", tagged_pages, name="tagged_pages"),
]
