# Интернет-магазин для деятельности ресторанов, услуги по доставке продуктов питания.
## Технология: Django Nginx Celery Redis Gunicorn Docker-Compose TeleBot Certbot

### Данный проект был разработан с целью автоматизации процесса заказа продуктов питания до потребителя. В процессе, были использованы различные технологии и инструменты:
Django - фреймворк разработки веб-приложений на языке Python.

Nginx - web-сервер, который широко применяется в обслуживании статического и динамического контента.

Celery+Redis — обеспечивают обработку задач в фоновом режиме: добавление нового ордера, отслеживание его статуса.

Gunicorn - запуска и управления web-приложения.

TeleBot - использовался для создания бота взаимодействия с полевыми сотрудниками через Telegram.

Каждый из перечисленных выше инструментов запущен и настроен в контейнере Docker. В процессе запуске магазина на сервере, добавлена возможность сознания SSL сертификата через Certbot с последующим его автоматическим обновлением.
Присутствует панель управления отслеживания новых заказов и их отправки до заказчика оператором + страница зала производства продукции. 

В завершении вступления и перед началом описания инструкции процесса установки магазина на сервер, нельзя не сказать  
о последней опции и это система приема платежей Yookassa. С её помощью вы будете безопасно принимать платежи, настроить чеки для налоговой и многое другое что значительно облегчит ведение вашего бизнеса. 