"""
Django settings for project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aj&yjl94f7w)_&7qgkkzk&24dftso&4o25jbw0@t9vtk^$z593'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['kice.kriea.co.kr']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'stdnt',
    'auth_ext',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        "ENGINE": "django.db.backends.mysql",
        "NAME":"kicekriea",
        "USER":"kicemaster",
        "PASSWORD":'j#jlIa81q',
        "HOST": "kicekriea.cxitgipj8rwq.ap-northeast-1.rds.amazonaws.com",
        "PORT": "3306",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'home/static'

INTERNAL_IPS = ("127.0.0.1",)

FABRIC = {
    "SSH_USER": "ubuntu", # SSH username for host deploying to
    "HOSTS": ALLOWED_HOSTS[:1], # List of hosts to deploy to (eg, first host)
    "DOMAINS": ALLOWED_HOSTS, # Domains for public site
    "REPO_URL": "ubuntu@kice.kriea.co.kr:/opt/git/kicekriea.git", # Project's repo URL
    "VIRTUALENV_HOME":  "/home/ubuntu/.virtualenvs", # Absolute remote path for virtualenvs
    "PROJECT_NAME": "kice_kriea", # Unique identifier for project
    "REQUIREMENTS_PATH": "",#"requirements.txt", # Project's pip requirements
    "GUNICORN_PORT": 8000, # Port gunicorn will listen on
    "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
    "DB_PASS": "j#jlIa81q", # Live database password
    #"ADMIN_PASS": "default", # Live admin user password
    "SECRET_KEY": SECRET_KEY,
    #"NEVERCACHE_KEY": NEVERCACHE_KEY,
    "DJANGO_USER":"kice_master"
}

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError as e:
    if "local_settings" not in str(e):
        raise e
