import datetime

from django import template

from activity.models import Activity


register = template.Library()


@register.simple_tag
def recent_activity():
    last_week = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=6)
    activity_counts = Activity.objects.counts_by_day().filter(created__gt=last_week)
    activity_list = []
    activity_dates = {a["activity_date"].date() for a in activity_list}
    for a in activity_counts:
        date = a["activity_date"].date()
        activity_list.append({"activity_date": date, "activities": a["activities"]})
        activity_dates.add(date)
    for day in range(7):
        date = (
            datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=day)
        ).date()
        if date not in activity_dates:
            activity_list.append({"activity_date": date, "activities": 0})
    return activity_list
