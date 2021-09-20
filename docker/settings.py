from .base_settings import *

INSTALLED_APPS += [
    'webpack_bridge',
    'compass.apps.CompassConfig'
]

STATICFILES_DIRS = [
    '/static/compass/',
]

DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default="")
LOGOUT_URL = os.getenv("LOGOUT_URL", default="")

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'compass.context_processors.google_analytics',
    'compass.context_processors.logout_url',
    'compass.context_processors.django_debug'
])

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

if os.getenv("ENV") == "localdev":
    DEBUG = True
    COMPASS_USERS_GROUP = 'u_test_group'
else:
    COMPASS_USERS_GROUP = os.getenv('ACCESS_GROUP', '')
