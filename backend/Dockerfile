FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app

# Installing Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copying the project files
COPY pyproject.toml poetry.lock /app/

# Installing the dependencies
RUN poetry install --no-root

# Copying the rest of the files
COPY . /app/

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["poetry", "run", "flask", "run"]