from django.apps import AppConfig


class TestConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "activity.test"
    label = "activity_test"
