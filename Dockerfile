FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

# Instala o Poetry
RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root


CMD ["gunicorn","loja_brinquedos.wsgi:application", "--bind", "0.0.0.0:8000"] 