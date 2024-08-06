FROM python:3.12-slim

# Creating the working directory
RUN mkdir /app
WORKDIR /app

# Installing dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Installing poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copying the project files
COPY pyproject.toml poetry.lock /app/

# Installing the package dependencies
RUN poetry install --no-root

# Copying the rest of the files
COPY ../ /app/

# Adding execute permissions to the entrypoint
RUN chmod +x /app/entrypoint.sh

# Exposing the port
EXPOSE 8000

# Running the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]