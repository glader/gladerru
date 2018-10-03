# coding: utf-8
# Django settings for gladerru project.
import os
import logging
import raven

BASE_DIR = os.path.dirname(__file__)

try:
    RELEASE = open(os.path.join(BASE_DIR, '..', 'release')).read()
except Exception:
    RELEASE = 'dev'

APPEND_SLASH = False

ADMINS = (('Glader', 'glader.ru@gmail.com'),)
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'glader.ru@gmail.com'

AUTH_PROFILE_MODULE = 'core.Profile'

FORCE_SCRIPT_NAME = ""
TIME_ZONE = 'Asia/Yekaterinburg'
LANGUAGE_CODE = 'ru-ru'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = '12345'
ROOT_URLCONF = 'urls'

DEBUG = False
TIMING = True
LOG_LEVEL = logging.WARNING
INTERNAL_IPS = ('127.0.0.1',)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

MIDDLEWARE = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.Redirection',
    'core.middleware.UserReferer',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/3')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',

                'core.context.profile',
                'core.context.domain',
            ],
        },
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'captcha',
    'django_russian',
    'gunicorn',
    'raven.contrib.django.raven_compat',
    'reversion',

    'core',
    'discounts',
    'mountains',
    'movies',
)

ALLOWED_HOSTS = ('glader.ru', 'glader_local.ru')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core', 'static'),
)

THUMBNAIL_ROOT = '/var/cache/gladerru/thumbnails'  # os.path.join(MEDIA_ROOT, 'data/thumbnails')
THUMBNAIL_URL = 'data/thumbnails/'
THUMBNAIL_SIZE = 300, 150

ALPHABET_LETTERS = [u'ABCDEFGHIJKLMNOPQRSTUVWXYZ', u'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ']

SOUNDTRACKS_PREFIX = 'http://glader-ru.s3.amazonaws.com/sound/'

LOGIN_URL = '/auth/login'

DESIGN_ID = 3
MAIN_PAGE_LEVEL = 1
SMILES = (':-?\)+', ':-?\(+', '\s:D+')

DOMAIN = 'glader.ru'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_ROOT = 'glader.ru/'
CACHE_LONG_TIMEOUT = 60 * 60 * 24  # Долгий таймаут, для практически не изменяющихся данных

VK_API_ID = 2009513

NOCAPTCHA = True

# Sentry
RAVEN_CONFIG = {
    'dsn': 'https://b05c4511cec248a38bc9bc4a52755013@sentry.io/265386',
    'release': RELEASE,
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format':
                '%(asctime)s %(name)-15s %(levelname)s %(message)s',
        }
    },
    'handlers': {
        'plain': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['plain', 'debug'],
            'level': 'DEBUG',
        },
        'py.warnings': {
            'level': 'ERROR'
        },
        'urllib3': {
            'level': 'WARNING'
        },
        'requests': {
            'level': 'WARNING'
        },
    }
}


try:
    from local_settings import *
except ImportError:
    pass
