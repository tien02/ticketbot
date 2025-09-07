ARG BASE_IMAGE=python:3.10-alpine

FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apk add --no-cache curl gcc musl-dev libffi-dev

WORKDIR /module

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./app /module/app
COPY ./config /module/config
COPY ./schema /module/schema
COPY ./src /module/src
COPY ./pyproject.toml /module/pyproject.toml

RUN pip install -e .
