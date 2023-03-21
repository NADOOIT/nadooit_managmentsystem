#TODO Check for new versions of the base image. If a new version is available, rebuild the image.
FROM python:3.10-alpine3.16
LABEL maintainer="nadooit.de"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt

RUN mkdir /app
COPY app/ /app

RUN apk add --upgrade --no-cache build-base --virtual .tmp gcc libc-dev linux-headers git curl
RUN unset https_proxy


RUN mkdir -p /vol/web/static/media
RUN mkdir -p /vol/web/static/static
RUN mkdir -p /home/django/.postgresql/

#OLD RUN adduser -D --disabled-password --no-create-home django
RUN adduser -D --disabled-password django

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


RUN pip install --upgrade pip && \
       pip install -r /requirements.txt &&\
       python manage.py collectstatic --noinput 
       #TODO #183 #182 check if this should be done in migrations or how to migrate server in production
       #&&\
       #python manage.py makemigrations &&\
       #python manage.py migrate

USER root

RUN pip install uwsgi
RUN apk del .tmp


USER django


CMD [ "uwsgi","--socket",":9090","--workers","4","--master","--enable-threads","--module","nadooit.wsgi" ]