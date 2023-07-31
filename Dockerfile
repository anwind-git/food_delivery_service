FROM python:3.10-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY shipping_service /shipping_service
WORKDIR /shipping_service
EXPOSE 8000

RUN pip install --upgrade pip

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user