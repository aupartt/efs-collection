# Utilise une image officielle Python comme base
FROM python:3.12-slim

# Installe Poetry
RUN pip install poetry

# Définit le répertoire de travail dans le conteneur
WORKDIR /api-carto-client

# Copie les fichiers de projet
COPY pyproject.toml ./

# Installe les dépendances
RUN poetry install --no-interaction --no-ansi --no-root

COPY . .
