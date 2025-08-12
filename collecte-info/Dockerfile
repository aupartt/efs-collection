FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

COPY ./api-carto-client /api-carto-client
COPY ./crawler /crawler

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./collecte-info/uv.lock,target=uv.lock \
    --mount=type=bind,source=./collecte-info/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

RUN uvx playwright install chromium --with-deps

# Add alembic for migration
COPY ./collecte-info/alembic.ini ./collecte-info/alembic.ini
COPY ./collecte-info/alembic ./collecte-info/alembic

# App
COPY ./collecte-info/collecte ./collecte-info/collecte
COPY ./collecte-info/cli.py ./collecte-info/cli.py

# Config
COPY ./collecte-info/uv.lock ./collecte-info/pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM builder

WORKDIR /app/collecte-info/

ENV PATH="/app/.venv/bin:$PATH"

# -u to enable log to be printed with docker compose run
ENTRYPOINT ["python", "-u", "-m"]