import factory
from factory.django import DjangoModelFactory

from wagtail_factories import SiteFactory

from analytics.models import AnalyticsSettings


class AnalyticsSettingsFactory(DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    umami_id = factory.Faker("uuid4")

    class Meta:
        model = AnalyticsSettings
