import os
import dj_database_url
from pathlib import Path
import dotenv

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY','dev_secret_key')

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'Fals'
FLUTTERWAVE_PRODUCTION = os.environ.get('FLUTTERWAVE_PRODUCTION', '') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost, 127.0.0.1').split(', ')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'core.apps.CoreConfig',
    'draw.apps.DrawConfig',
    'transaction.apps.TransactionConfig',
    'wallet.apps.WalletConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'raffle.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'raffle.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

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

AUTH_USER_MODEL = 'core.CustomUser'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = BASE_DIR / 'staticfiles' 

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Email Settings
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'TestEmail@raffle.com')

# Some Development settings
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FLUTTERWAVE_SECRET_KEY = os.environ.get('FLUTTERWAVE_PRODUCTION_SECRET_KEY','') if FLUTTERWAVE_PRODUCTION else os.environ.get('FLUTTERWAVE_TEST_SECRET_KEY','')
ENV_ID =  os.environ.get('ENV_ID', 0)

# Mailing Set up
GMAIL_USED = os.environ.get('GMAIL_USED', "") == "True"
EMAIL_HOST="smtp.gmail.com"
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_PORT=587
EMAIL_HOST_USER=os.environ.get("EMAIL_HOST_USER","")
EMAIL_HOST_PASSWORD=os.environ.get("EMAIL_HOST_PASSWORD","")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'