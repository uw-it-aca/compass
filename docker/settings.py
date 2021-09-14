from .base_settings import *

INSTALLED_APPS += [
    'webpack_bridge',
    'compass.apps.CompassConfig'
]

STATICFILES_DIRS = [
    '/static/compass/',
]

DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

TEMPLATES['OPTIONS']['context_processors'].extend([
    'compass.context_processors.google_analytics',
    'compass.context_processors.django_debug'
])

if os.getenv("ENV") == "localdev":
    DEBUG = True
    COMPASS_USERS_GROUP = "u_test_group"

EDW_USERNAME = os.getenv("EDW_USERNAME", default=" ")
EDW_PASSWORD = os.getenv("EDW_PASSWORD", default=" ")
EDW_HOSTNAME = os.getenv("EDW_HOSTNAME", default=" ")
