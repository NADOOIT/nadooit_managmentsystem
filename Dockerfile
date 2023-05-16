#TODO Check for new versions of the base image. If a new version is available, rebuild the image.
FROM python:3.10-slim-buster
LABEL maintainer="nadooit.de"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN mkdir /app
COPY app/ /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    gcc \
    libc-dev \
    linux-headers-amd64 \
    ffmpeg

RUN unset https_proxy

# Create the directories for static and media files
RUN mkdir -p /vol/web/static/media
RUN mkdir -p /vol/web/static/static
RUN mkdir -p /home/django/.postgresql/

#OLD RUN adduser -D --disabled-password --no-create-home django
RUN adduser --disabled-password --gecos "" django

RUN chown -R django:django app/
RUN chown -R django:django /vol

RUN chmod -R 755 app/
RUN chmod -R 755 /vol/web
WORKDIR /app

EXPOSE 8000

RUN chown -R django:django /app
RUN chown -R django:django /home/django
RUN chmod 755 /home/django
RUN chmod 755 /app

USER django

RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install -r /requirements.txt 
RUN python manage.py collectstatic --noinput 

USER root
RUN pip install uwsgi

USER django

CMD [ "uwsgi","--socket",":9090","--workers","4","--master","--enable-threads","--module","nadooit.wsgi" ]
