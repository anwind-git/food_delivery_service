FROM python:3.10-alpine3.18

COPY requirements.txt /temp/requirements.txt
RUN apk update && apk upgrade && \
    apk add --no-cache bash postgresql-client && \
    apk add --no-cache --virtual .build-deps build-base postgresql-dev && \
    pip install --upgrade pip && \
    pip install gunicorn && \
    pip install -r /temp/requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*

COPY shipping_service /shipping_service
WORKDIR /shipping_service
RUN adduser --disabled-password service-user
USER service-user

EXPOSE 8000
CMD ["gunicorn", "shipping_service.wsgi:application", "--bind", "0.0.0.0:8000"]
