"""
Файл конфигурации Celery для службы доставки еды.
"""
import os
import time
from celery import Celery
from django.conf import settings

# Установка переменной окружения для 'DJANGO_SETTINGS_MODULE'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shipping_service.settings')

# Создание экземпляра Celery и его конфигурация из Django settings.
app = Celery('shipping_service')
app.config_from_object('django.conf:settings')

# Установка URL брокера из Django settings.
app.conf.broker_url = settings.CELERY_BROKER_URL

# Включение повторной попытки подключения к брокеру при старте.
app.conf.broker_connection_retry_on_startup = True

# Автоматическое обнаружение и регистрация задач в Django приложениях.
app.autodiscover_tasks()


@app.task()
def debug_task():
    """
    Пример задачи Celery для отладки.
    """
    time.sleep(20)
    print('Hello form debug_task')
