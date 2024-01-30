import urllib3
import asyncio
import requests.exceptions
from django.core.management.base import BaseCommand
from bot import bot

urllib3.disable_warnings()
urllib3.PoolManager().connection_pool_kw['timeout'] = 60


class Command(BaseCommand):
    help = 'Телеграм бот службы доставки'

    def handle(self, *args, **options):
        try:
            asyncio.run(bot.polling(none_stop=True))
        except requests.exceptions.ReadTimeout as e:
            print("Произошла ошибка ReadTimeout при обращении к API Telegram:", e)
        except urllib3.exceptions.MaxRetryError as e:
            print("Произошла ошибка MaxRetryError:", e)
        except urllib3.exceptions.NameResolutionError as e:
            print("Произошла ошибка разрешения имени (NameResolutionError):", e)

