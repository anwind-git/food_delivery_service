FROM python:3.10-alpine3.18

COPY requirements.txt /temp/requirements.txt
COPY shipping_service /shipping_service
WORKDIR /shipping_service
EXPOSE 8000

RUN apk update && apk upgrade && apk add bash
RUN pip install --upgrade pip
RUN pip install gunicorn
CMD ["gunicorn", "shipping_service.wsgi:application", "--bind", "0.0.0.0:8000"]

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user
RUN adduser service-user www-data
USER service-user
