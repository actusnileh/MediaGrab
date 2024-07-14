FROM python:3.11-buster

ENV PYTHONDONTWRITEBYTECODE  1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

RUN wget -O /tmp/ffmpeg-release-amd64-static.tar.xz https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar -xJf /tmp/ffmpeg-release-amd64-static.tar.xz -C /tmp \
    && cp /tmp/ffmpeg-*/ffmpeg /usr/local/bin/ \
    && cp /tmp/ffmpeg-*/ffprobe /usr/local/bin/ \
    && rm -rf /tmp/ffmpeg-*

RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

VOLUME /app/videos

COPY . .
