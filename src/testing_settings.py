# development
from __future__ import unicode_literals

from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'log/email'

SECRET_KEY = '12345'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'upload')

try:
    os.makedirs(EMAIL_FILE_PATH)
except Exception:
    pass

LOG_PATH = 'log'
LOG_LEVEL = logging.DEBUG

for name, handler in LOGGING['handlers'].items():
    if 'filename' in handler:
        handler['filename'] = os.path.join(LOG_PATH, os.path.basename(handler['filename']))

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
