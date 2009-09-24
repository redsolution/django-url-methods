import os

DEBUG = False

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'urlmethods.sqlite'
SITE_ID = 1

SECRET_KEY = '2j17u@ngrc0=bzsp-02p^@(026w^6ec(rbfw^*wdk009fc1@w_'

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'urlmethods',
    'example',
)
