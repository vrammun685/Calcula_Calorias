from .base import *

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Base de datos local
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
