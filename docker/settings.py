from .base_settings import *

INSTALLED_APPS += [
    'compass.apps.CompassConfig',
    'simple_history',
    'webpack_loader',
]

# Location of stats file that can be accessed during local development and 
# collected from during production build process
if os.getenv("ENV") == "localdev":
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, 'compass/static/webpack-stats.json'),
        }
    }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.join(BASE_DIR, "compass"),
                                 'db.sqlite3'),
        }
    }
else:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, '/static/webpack-stats.json'),
        }
    }

# If you have file data, define the path here
DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

# Override default django User model
AUTH_USER_MODEL = 'compass.User'

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default="")
LOGOUT_URL = os.getenv("LOGOUT_URL", default="")

TEMPLATES[0]["OPTIONS"]["context_processors"].extend(
    [
        "compass.context_processors.google_analytics",
        "compass.context_processors.logout_url",
        "compass.context_processors.django_debug",
    ]
)

if os.getenv("ENV") == "localdev":
    DEBUG = True
    COMPASS_USERS_GROUP = "u_test_group"
else:
    COMPASS_USERS_GROUP = os.getenv('ACCESS_GROUP', '')
