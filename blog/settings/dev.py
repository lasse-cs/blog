# ruff: noqa: F403, F405

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3=_$m44l@^+c_!$4o@*moeurqpqyb@bmv#v+_6(bi9vdlur%^w"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += [
    # Django Pattern Library
    "pattern_overrides",
    "pattern_library",

    # Django Browser Reload
    "django_browser_reload",
]

TEMPLATES[0]["OPTIONS"]["builtins"] = [
    "pattern_library.loader_tags",
]

X_FRAME_OPTIONS = "SAMEORIGIN"

PATTERN_LIBRARY = {
    "SECTIONS": (
        ("components", ["patterns/components"]),
        ("pages", ["patterns/pages"]),
    ),
    "TEMPLATE_SUFFIX": ".html",
    "PATTERN_BASE_TEMPLATE_NAME": "patterns/base_pattern.html",
    "BASE_TEMPLATE_NAMES": ["patterns/base.html"],
}

MIDDLEWARE += [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

try:
    from .local import *
except ImportError:
    pass
