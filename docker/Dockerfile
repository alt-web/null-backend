FROM python:3.11-alpine

RUN apk add libmagic
RUN apk add ffmpeg

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 

RUN python manage.py collectstatic --noinput

ENV DJANGO_PRODUCTION=1
EXPOSE 8000

LABEL org.opencontainers.image.source https://github.com/alt-web/null-backend

ENTRYPOINT python manage.py migrate && exec gunicorn nullchan_backend.wsgi -b 0.0.0.0:8000
