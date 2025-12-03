FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN useradd wagtail
WORKDIR /app
EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    UV_LINK_MODE=copy \
    UV_NO_SYNC=1 \
    DJANGO_SETTINGS_MODULE="blog.settings.production"

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
libjpeg62-turbo \
zlib1g \
libwebp7 \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /app/static/ /app/media/
RUN chown -R wagtail:wagtail /app

COPY --chown=wagtail:wagtail ./pyproject.toml /app/pyproject.toml
COPY --chown=wagtail:wagtail ./uv.lock /app/uv.lock

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ADD --chown=wagtail:wagtail . /app

USER wagtail

CMD ["gunicorn", "--bind", ":8000", "blog.wsgi:application"]