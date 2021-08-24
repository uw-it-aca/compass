from .base_settings import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'webpack_bridge',
    'compass'
]

STATICFILES_DIRS = [
    '/static/compass/',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'compass.context_processors.google_analytics',
                'compass.context_processors.django_debug',
            ],
        }
    }
]

if os.getenv("ENV") == "localdev":
    DEBUG = True
