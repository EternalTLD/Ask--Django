FROM python:3.10-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache postgresql-libs postgresql-client libffi-dev
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN pip install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . .

ENTRYPOINT [ "/entrypoint.sh" ]