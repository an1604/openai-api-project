FROM postgres:15-alpine

COPY ./01-create-tables.sql /docker-entrypoint-initdb.d/
COPY ./02-seed-tables.sql /docker-entrypoint-initdb.d/

ARG CURRENT_VERSION
LABEL version=$CURRENT_VERSION
