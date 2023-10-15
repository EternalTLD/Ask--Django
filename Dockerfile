FROM python:3.10-alpine3.18

COPY requirements.txt /temp/requirements.txt

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password ask-user

USER ask-user

COPY ask_project /ask_project

WORKDIR /ask_project

EXPOSE 8000