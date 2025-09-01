FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

COPY ./api-carto-client /api-carto-client
COPY ./crawler /crawler

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Config
COPY ./collecte-info/uv.lock ./collecte-info/pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# App
COPY ./collecte-info/collecte ./collecte
COPY ./collecte-info/cli.py ./cli.py

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1


# -u to enable log to be printed with docker compose run
ENTRYPOINT ["python", "-u", "-m", "cli"]