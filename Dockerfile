FROM ubuntu:20.04

ENV PYTHONUNBUFFERED 1

# Install required packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV FLASK_APP=./app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN mkdir -p /app
WORKDIR /app

COPY ./requirements.txt /app
RUN pip3 install --upgrade pip==22.0.4
RUN pip3 install --upgrade setuptools==59.6.0
RUN pip3 install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run"]
