# syntax=docker/dockerfile:1

FROM debian:latest
# LABEL maintainer "Avi Kumar @avikumar15"

# Set a working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt
COPY credentials.json credentials.json

RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3-setuptools \
    python3-pip \
    nano

RUN pip3 install -r requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install quick-mail
