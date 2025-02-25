from pathlib import Path
from .base import *
import os
from decouple import config

DEBUG = False

ALLOWED_HOSTS = ['vrm.ieshm.org']

# Cargar credenciales desde .env
DB_NAME = config('DB_NAME', default=None)
DB_USER = config('DB_USER', default=None)
DB_PASSWORD = config('DB_PASSWORD', default=None)
DB_HOST = config('DB_HOST', default='localhost')
DB_PORT = config('DB_PORT', default='3306')

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',  # O 'django.db.backends.mysql' si usas mysqlclient
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD':DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

