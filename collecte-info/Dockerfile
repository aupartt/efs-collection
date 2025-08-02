FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copie le wheel depuis l'image api-carto-client
COPY ./api-carto-client /api-carto-client

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Installe les dépendances du projet en utilisant le lockfile et les paramètres
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=./collecte-info/uv.lock,target=uv.lock \
    --mount=type=bind,source=./collecte-info/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Ajoute le reste du code source du projet et l'installe
COPY ./collecte-info/*.py .
COPY ./collecte-info/uv.lock ./collecte-info/pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place les exécutables dans l'environnement au début du chemin
ENV PATH="/app/.venv/bin:$PATH"

# Réinitialise le point d'entrée, n'invoque pas `uv`
ENTRYPOINT ["python"]