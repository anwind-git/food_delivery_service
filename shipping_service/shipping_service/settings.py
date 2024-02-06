import os
import math
from pathlib import Path
from decimal import Decimal

from environs import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CART_SESSION_ID = 'cart'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
env = Env()
env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
"""
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
"""


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = ['127.0.0.1']
INTERNAL_IPS = ["127.0.0.1"]

TOKEN_BOT = env.str('TOKEN_BOT')  # Подключаем токен от телеграм бота

# Подключение Юкасса
ACCOUNT_YOOKASSA = env.str('ACCOUNT_YOOKASSA')  # ID Юкасса
SECRET_KEY_YOOKASSA = env.str('SECRET_KEY_YOOKASSA')  # Секретный ключ Юкасса

# Подключение подсказок адресов клиентов для доставки еды
TOKEN_ID_DADATA = env.str('TOKEN_ID_DADATA')
SECRET_DADATA = env.str('SECRET_DADATA')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'shop_app.apps.ShopAppConfig',
    'cart.apps.CartConfig',
    'organization.apps.OrganizationConfig',
    'recipes.apps.RecipesConfig',
    'orders.apps.OrdersConfig',
    'management.apps.ManagementConfig',
    "debug_toolbar",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'shipping_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'shipping_service.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = 'redis://redis:6379/0'

AUTH_USER_MODEL = 'organization.UserProfile'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

"""
def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION':  BASE_DIR /"cache",
    }
}


# Настройки магазина
SITE_NAME = 'Demo Магазин'  # название магазина(сайта)
SHOP_CURRENCY = 'руб.'  # валюта, выводиться на страницах магазина
SINGLE_TELEPHONE_NUMBER = '+7(000) 000-00-00'  # единый телефон поддержки
DENIAL_SERVICE = (
        (1, 'ЗАКАЗ ОТМЕНЕН КЛИЕНТОМ'),
        (2, 'ЗАКАЗ НЕ ПОДТВЕРЖДЕН'),
        (3, 'В АДРЕСЕ ДОСТАВКИ УКАЗАН НЕ ВЕРНЫЙ ГОРОД')
    )  # причины для отказа доставки заказа, возврат средств
COMMISSION_FREE_PRICE = 200  # стоимость доставки заказа без комиссии юкасса
CACHE_TIME = 60  # время кэширования в секундах
RESPONSE_TIME = 600  # Время в секундах, которое дается сотруднику на ответ, принимает он заказ или нет.

# Настройки Юкасса https://yookassa.ru/developers/payment-acceptance/receipts/54fz/other-services/parameters-values
COMMISSION = 0.037  # комиссия Юкасса за проведение операции

# стоимость доставки с комиссией от юкасса
SHIPPING_COST = math.ceil(Decimal(COMMISSION_FREE_PRICE) * Decimal(1 + COMMISSION))

FIAT_CURRENCY = 'RUB'  # валюта для Юкасса
METHOD_PAYMENT = 'bank_card'  # метод оплаты
TAX_SYSTEM_CODE = '2'  # Коды систем налогообложения
VAT_CODE = '3'  # Код ставки НДС
PAYMENT_MODE = 'full_prepayment'  # признак способа расчета
PAYMENT_SUBJECT = 'commodity'  # признак предмета расчета
COUNTRY_OF_ORIGIN_CODE = 'RU'  # код страны происхождения
MEASURE = 'piece'  # Мера количества предмета расчета

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process} {thread} {message}', 'style': '{',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/shipping_service/log/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'shop_app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'orders': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cart': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

