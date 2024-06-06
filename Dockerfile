FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE  1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get install && apt-get install -y python

RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

COPY . .