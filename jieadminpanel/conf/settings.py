import os
from pathlib import Path

from app_files.conf.secretkey import *
from app_files.conf.apps_installed import APPS_INSTALLED_LIST
from app_files.conf.encryptionkey import *

from .additionals import *

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appcommon',
    'panel.systemauth',
    'panel.panelhome',
    'panel.appstore',
    'panel.module_envs',
    'panel.module_database',
    'panel.module_system',
]
for app in APPS_INSTALLED_LIST:
    INSTALLED_APPS.append(f'apps.{app}')

APPS_ROOT = Path.joinpath(BASE_DIR, 'apps')

# for app in APPS_LIST:
#     INSTALLED_APPS.append(f'apps.{app}')

# app_name = [d for d in os.listdir(app_dir) if os.path.isdir(os.path.join(app_dir, d))]
# for dir_name in os.listdir(APPS_ROOT):
#     if os.path.isdir(os.path.join(APPS_ROOT, dir_name)):
#         INSTALLED_APPS.append(f'apps.{dir_name}')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

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

WSGI_APPLICATION = 'conf.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db',
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

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = False
USE_TZ = False

DATE_FORMAT = 'Y-m-d'
SHORT_DATE_FORMAT = 'Y/m/d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i:s'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/home/index/'
LOGOUT_REDIRECT_URL = '/login/'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# SESSION_COOKIE_AGE = 60 * 60
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'app_files'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'systemauth.Users'

VERSION = '0.0.1-a'

SYSTEM_VERBOSE_NAME = 'JieAdmin控制面板'

