from django.urls import path


from activity.views import activity_index


urlpatterns = [
    path("", activity_index, name="activity_index"),
]
