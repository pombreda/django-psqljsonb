import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'asdfalskdfjasldkfjalskfjaslkjfdlakjdflkajsdlfkjasl'

DATABASES = {
    'default': {
        # possible backends are:
        #   * django.db.backends.postgresql_psycopg2
        #   * django.contrib.gis.db.backends.postgis
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'jsonbtest',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    },
}

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin.apps.AdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'psqljsonb',
    'psqljsonb.tests',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

