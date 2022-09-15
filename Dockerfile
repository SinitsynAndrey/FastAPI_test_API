FROM python:alpine

ENV PYTHONBUFFERED 1

EXPOSE 8080
WORKDIR /app

COPY . .

RUN apk add build-base
RUN pip install -e .
