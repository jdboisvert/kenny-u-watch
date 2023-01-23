FROM python:3.9-alpine3.13
LABEL maintainer="info.jeffreyboisver@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY . /user_watch_management

WORKDIR /user_watch_management
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home user_watch_management

ENV PATH="/py/bin:$PATH"

USER user_watch_management
