"""
Django settings for freelancefinder application.

Requires django-environ
"""

import environ

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env(root('.env'))

BASE_DIR = root()

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

# TODO: Set this appropriately
ALLOWED_HOSTS = ['*']

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authtools',
    'django_celery_beat',
    'crispy_forms',
]

PROJECT_APPS = [
    'jobs',
    'remotes',
    'users',
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

# Enable authtools
AUTH_USER_MODEL = 'authtools.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'freelancefinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'freelancefinder.wsgi.application'

DATABASES = {
    'default': env.db()
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
    },
    'formatters': {
        'main': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            # Since we're doing json logging, just throw everything in there
            'format': '''
                %(threadName)s %(name)s %(thread)d %(created)f
                %(process)d %(processName)s %(relativeCreated)f
                %(module)s %(funcName)s %(levelno)d %(msecs)f
                %(pathname)s %(lineno)d %(asctime)s %(message)s
                %(filename)s %(levelname)s %(request_id)s
            ''',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
        'celery': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            # Since we're doing json logging, just throw everything in there
            'format': '''
                %(threadName)s %(name)s %(thread)d %(created)f
                %(process)d %(processName)s %(relativeCreated)f
                %(module)s %(funcName)s %(levelno)d %(msecs)f
                %(pathname)s %(lineno)d %(asctime)s %(message)s
                %(filename)s %(levelname)s
            ''',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'email': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false', 'request_id'],
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/freelancefinder.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main',
            'filters': ['require_debug_false', 'request_id'],
        },
        'celery': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/freelancefinder_celery.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'celery',
            'filters': ['require_debug_false'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'main',
            'filters': ['require_debug_true', 'request_id'],
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django_debug.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'formatter': 'main',
            'filters': ['require_debug_true', 'request_id'],
        },
        'null': {
            "class": 'logging.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['email', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['null', ],
        },
        'celery': {
            'handlers': ['console', 'celery', 'debug'],
            'level': 'DEBUG',
        },
        'py.warnings': {
            'handlers': ['null', ],
        },
        '': {
            'handlers': ['console', 'logfile', 'debug'],
            'level': "DEBUG",
        },
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

# Celery settings
BROKER_URL = env('REDIS_CELERY_URL')
CELERY_RESULT_BACKEND = env('REDIS_CELERY_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

public_root = root.path('public/')

MEDIA_ROOT = public_root('media')
MEDIA_URL = 'media/'

STATIC_ROOT = public_root('static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [root('static')]
