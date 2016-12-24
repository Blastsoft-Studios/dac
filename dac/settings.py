import os
import configparser
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, 'settings.ini')

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

allowed_hosts = config.get('App', 'allowed_hosts')
ALLOWED_HOSTS = allowed_hosts.split(' ')

TEMPLATES_DIRS = [os.path.join(BASE_DIR, 'templates')]
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'

DEBUG = config.getboolean('App', 'debug')
SECRET_KEY = config.get('App', 'secret')
STATIC_ROOT = config.get('App', 'static_root')

ROOT_URLCONF = 'home.urls'
WSGI_APPLICATION = 'dac.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: %(message)s",
            'datefmt': "%Y/%m/%d/ %H:%M:%S"
        },
        'stats': {
            'format': "%(asctime)s: %(message)s",
            'datefmt': "%Y/%m/%d/ %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': config.get('Logging', 'level'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': config.get('Logging', 'file'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'statfile': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': config.get('Logging', 'stats'),
            'formatter': 'stats',
        },
    },
    'loggers': {
        'django': {
            'handlers':['logfile'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['logfile'],
            'level': config.get('Logging', 'level'),
            'propagate': False,
        },
        'dac': {
            'handlers': ['logfile'],
            'level': config.get('Logging', 'level'),
        },
        'stats': {
            'handlers': ['statfile'],
            'level': 'INFO',
        },
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATES_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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
