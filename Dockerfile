FROM python:3.8-alpine

WORKDIR /app
COPY . /app/

ENV DJANGO_SETTINGS_MODULE=project.settings

RUN apk update

RUN pip install --upgrade -r requirements.txt
RUN apk update && apk add bash

CMD ["python"]