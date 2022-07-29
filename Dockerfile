ARG DJANGO_CONTAINER_VERSION=1.4.1

FROM gcr.io/uwit-mci-axdd/django-container:${DJANGO_CONTAINER_VERSION} as app-prewebpack-container

USER root

RUN apt-get update && apt-get install libpq-dev -y
# COPY docker/locations.conf /etc/nginx/includes/locations.conf

USER acait

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/

ADD --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh

RUN /app/bin/pip install -r requirements.txt
RUN /app/bin/pip install psycopg2

FROM node:14.18.1-stretch AS wpack

ADD ./package.json /app/
WORKDIR /app/
RUN npm install .

ADD . /app/

ARG VUE_DEVTOOLS
ENV VUE_DEVTOOLS=$VUE_DEVTOOLS
RUN npx webpack --mode=production

FROM app-prewebpack-container as app-container

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/
COPY --chown=acait:acait --from=wpack /app/compass/static /static

RUN . /app/bin/activate && python manage.py collectstatic --noinput

FROM gcr.io/uwit-mci-axdd/django-test-container:${DJANGO_CONTAINER_VERSION} as app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
