#TODO Check for new versions of the base image. If a new version is available, rebuild the image.
FROM nginx:1.23.0-alpine

#TODO rights managment seems to be wrong. Should be a less privileged user
#FROM nginxinc/nginx-unprivileged:1.23.0-alpine


COPY ./nginx/* /etc/nginx/
COPY run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=9090

RUN apk add --no-cache openssl bash
RUN chmod +x /run.sh

RUN mkdir -p /vol/web/static
RUN chmod -R 755 /vol/web/static

RUN mkdir -p /vol/web/media
RUN chmod -R 755 /vol/web/media


VOLUME /vol/web
VOLUME /vol/www


CMD ["/run.sh"]