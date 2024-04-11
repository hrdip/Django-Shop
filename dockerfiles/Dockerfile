# image used for this project
FROM python:3.11-slim-buster 

# who made this project
LABEL maintainer="hrdip.2018@gmail.com"

# when we want show something in console, they buffering. and 1 means True value
ENV PYTHONUNBUFFERED=1

# this directory for developing my web app
WORKDIR /usr/src/app

# copy requirements.txt file from main directory(first .) to WORKDIR (second .)
COPY ./requirements.txt .

# do this command
RUN pip install --upgrade pip && pip install -r requirements.txt

# move core directory (main project dir) to WORKDIR 
COPY ./core .