# syntax=docker/dockerfile:1
FROM python:3.8-alpine

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev \
    libffi-dev openssl-dev

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

ENV FLASK_APP=./app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
