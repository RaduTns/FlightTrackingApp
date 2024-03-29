"""
Django settings for FlightTrackingApp project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$%r-b$%frb6y=_&h&_%q#c%5h3_qg9zxhpc$r6nvceef$@%c3t'

API_USERNAME = 'TanaseRadu'

API_PASSWORD = '5fYLPthGn@YAxn6'

GOOGLE_MAPS_API = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyBXY08Mo2gHV7jrkFSaqAaB4bguOYgdOJ4&callback=initMap&libraries=places'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True


ALLOWED_HOSTS = []
#LOGIN_REDIRECT_URL = '/profile/'
AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of allauth
    'django.contrib.auth.backends.ModelBackend',

    # allauth specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]
#ACCOUNT_SIGNUP_REDIRECT_URL = "http://localhost:8000/profile/keycloak/login/?process=login"
LOGIN_REDIRECT_URL='http://localhost:8000/home/'
LOGIN_URL = 'http://localhost:8000/profile/keycloak/login/?process=login'
LOGOUT_REDIRECT_URL = '/accounts/logged-out'
# Application definition



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'FlightTrackingApp',
    'DB_work',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.keycloak',
    'channels',
    
]

SITE_ID = 2

# Set your keycloak url and realm
SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': 'http://localhost:8080',
        'KEYCLOAK_REALM': 'master'
    }
}
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FlightTrackingApp.urls'

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

WSGI_APPLICATION = 'FlightTrackingApp.wsgi.application'
ASGI_APPLICATION = 'FlightTrackingApp.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, "DB_work/static")