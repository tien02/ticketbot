ARG BASE_IMAGE=pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime

FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /module

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./app /module/app
COPY ./config /module/config
COPY ./schema /module/schema
COPY ./src /module/src
COPY ./pyproject.toml /module/pyproject.toml

RUN pip install -e .
