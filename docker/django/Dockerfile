FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd wagtail

ENV DJANGO_SETTINGS_MODULE="blog.settings.production"

EXPOSE 8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    libwebp7 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN chown wagtail:wagtail /app

COPY --chown=wagtail:wagtail ./pyproject.toml /app/pyproject.toml
COPY --chown=wagtail:wagtail ./uv.lock /app/uv.lock

ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_NO_SYNC=1

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ADD --chown=wagtail:wagtail . /app

USER wagtail

CMD ["gunicorn", "blog.wsgi:application", "0.0.0.0:8000"]