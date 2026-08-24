import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')


def env_value(name, default=''):
    file_path = os.environ.get(f'{name}_FILE')
    if file_path:
        try:
            return Path(file_path).read_text().strip()
        except OSError:
            return default
    value = os.environ.get(name)
    return default if value in (None, '') else value


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value in (None, ''):
        return default
    return value.lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=None):
    value = os.environ.get(name)
    if value in (None, ''):
        return default or []
    return [item.strip() for item in value.split(',') if item.strip()]


SECRET_KEY = env_value('SECRET_KEY', default='django-insecure-dev-only-change-me')

DEBUG = env_bool('DEBUG', default=False)

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
CSRF_TRUSTED_ORIGINS = env_list(
    'CSRF_TRUSTED_ORIGINS',
    default=['http://localhost', 'http://127.0.0.1'],
)


# Application definition

INSTALLED_APPS = [
    'base',
    'brokerages',
    'accounts',
    'clients',
    'insurers',
    'branches',
    'covered_items',
    'proposals',
    'policies',
    'claims',
    'attachments',
    'crm',
    'renewals',
    'endorsements',
    'commissions',
    'reports',
    'dashboard',
    'ai_agents',
    'notifications',
    'dj_celery_panel',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'base.middleware.CurrentBrokerageMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

database_url = env_value('DATABASE_URL')
if database_url:
    DATABASES = {'default': env.db('DATABASE_URL')}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }


# Cache

REDIS_URL = env_value('REDIS_URL', default='redis://redis:6379/0')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    },
}


# Celery

CELERY_BROKER_URL = env_value(
    'CELERY_BROKER_URL',
    default='amqp://scsi:scsi@rabbitmq:5672/scsi',
)
CELERY_RESULT_BACKEND = env_value(
    'CELERY_RESULT_BACKEND',
    default='redis://redis:6379/1',
)
CELERY_TIMEZONE = TIME_ZONE if 'TIME_ZONE' in globals() else env_value(
    'TIME_ZONE',
    default='America/Sao_Paulo',
)
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'health_check'
LOGOUT_REDIRECT_URL = 'accounts:login'


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = env_value('TIME_ZONE', default='America/Sao_Paulo')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = Path(env_value('STATIC_ROOT', default=str(BASE_DIR / 'staticfiles')))

MEDIA_URL = 'media/'
MEDIA_ROOT = Path(env_value('MEDIA_ROOT', default=str(BASE_DIR / 'media')))


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

MAILERS = {
    'default': {
        'BACKEND': env_value(
            'EMAIL_BACKEND',
            default='django.core.mail.backends.console.EmailBackend',
        ),
        'HOST': env_value('EMAIL_HOST'),
        'PORT': int(env_value('EMAIL_PORT', default='587')),
        'USERNAME': env_value('EMAIL_HOST_USER'),
        'PASSWORD': env_value('EMAIL_HOST_PASSWORD'),
        'USE_TLS': env_bool('EMAIL_USE_TLS', default=True),
    },
}

DEFAULT_FROM_EMAIL = env_value('DEFAULT_FROM_EMAIL', default='no-reply@scsi.digital')

SECURE_REDIRECT_EXEMPT = [r'^health/$']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

OPENAI_API_KEY = env_value('OPENAI_API_KEY')
OPENAI_MODEL = env_value('OPENAI_MODEL', default='GPT-5.5-mini')
