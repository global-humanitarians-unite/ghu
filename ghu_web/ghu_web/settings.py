"""
Django settings for ghu_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from configparser import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Need to disable interpolation so that `%'s in the secret_key don't
# confuse the parser, which will try to treat them as %(interpolation)s
cfg = ConfigParser(interpolation=None)
# Preserve case
cfg.optionxform = str
if not cfg.read(os.path.join(BASE_DIR, 'config.ini')):
    raise FileNotFoundError('config.ini does not exist. Please create it as described in the README')

SECRET_KEY = cfg['secrets']['secret_key']

if 'production' in cfg:
    ALLOWED_HOSTS = cfg['production']['hosts'].split()
else:
    ALLOWED_HOSTS = []

# Disable debug mode if the hosts setting exists and is nonempty
DEBUG = not bool(ALLOWED_HOSTS)

# Where to collect static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Configure SMTP if [mail] section exists in config.ini
if 'mail' in cfg:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    sec = cfg['mail']
    EMAIL_HOST = sec['host']
    EMAIL_PORT = sec.get('port', None)
    # SSL connection (implicit)
    EMAIL_USE_SSL = sec.get('use_ssl', '').lower() == 'true'
    # STARTTLS (explicit)
    EMAIL_USE_TLS = sec.get('use_tls', '').lower() == 'true'
    EMAIL_HOST_USER = sec['user']
    EMAIL_HOST_PASSWORD = sec['password']
else:
    # If not configured (development), print emails to the console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email error messages to the configured addresses
if 'admins' in cfg:
    ADMINS = [ (name, addr) for name, addr in cfg['admins'].items() ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ordered_model',
    'ghu_global',
    'ghu_main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ghu_web.urls'

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
                'django_settings_export.settings_export',
            ],
        },
    },
]

WSGI_APPLICATION = 'ghu_web.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# We don't know BASE_DIR in config.ini, so we can't include it in the path to
# the sqlite3 database. So if the engine is sqlite3 and `name' is a relative
# path, prepend BASE_DIR to it
if cfg['db']['engine'] == 'sqlite3' and 'name' in cfg['db'] \
                                    and not os.path.isabs(cfg['db']['name']):
    cfg['db']['name'] = os.path.join(BASE_DIR, cfg['db']['name'])

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + cfg['db']['engine'],
        'NAME': cfg['db'].get('name', None),
        'USER': cfg['db'].get('user', None),
        'PASSWORD': cfg['db'].get('password', None),
        'HOST': cfg['db'].get('host', None),
        'PORT': cfg['db'].get('port', None),
    }
}

LOGOUT_REDIRECT_URL = '/'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'ghu_global.User'

# Settings to pass through to templates
# https://pypi.python.org/pypi/django-settings-export

SETTINGS_EXPORT = [
    'FEEDBACK_FORM_URL',
]

FEEDBACK_FORM_URL = 'https://goo.gl/forms/OtvG7Y8OFtUmBPaR2'
