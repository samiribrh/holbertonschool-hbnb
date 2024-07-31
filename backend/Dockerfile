FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

# Installing dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installing poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copying the project files
COPY pyproject.toml poetry.lock /app/

# Installing the dependencies
RUN poetry install --no-root

# Copying the rest of the files
COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "-w", "1", "--threads", "1", "-b", "0.0.0.0:8000", "app:app"]