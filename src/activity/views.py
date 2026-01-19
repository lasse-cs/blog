from itertools import groupby

from django.shortcuts import render

from activity.models import Activity
from core.utilities import paginate


def activity_index(request):
    activities = Activity.objects.all()
    page_number = request.GET.get("page", 1)
    pagination_page, page_range = paginate(page_number, activities)
    activities_by_day = {
        date: list(group)
        for date, group in groupby(
            pagination_page, lambda activity: activity.created.date
        )
    }
    context = {
        "pagination_page": pagination_page,
        "page_range": page_range,
        "activities_by_day": activities_by_day,
    }
    return render(request, "patterns/pages/activity/activity_index.html", context)
