# ruff: noqa: F403, F405

from .base import *
import tempfile

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3=_$m44l@^+c_!$4o@*moeurqpqyb@bmv#v+_6(bi9vdlur%^w"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [
    "activity.test",
    "core.test",
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_ROOT = tempfile.gettempdir()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
        "TEST": {
            # Don't use in-memory sqlite database
            # So that possible to reuse the DB
            "NAME": "test_db.sqlite3",
        },
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

UMAMI_HOST = None

try:
    from .local import *
except ImportError:
    pass
