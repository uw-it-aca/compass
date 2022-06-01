from .base_settings import *

INSTALLED_APPS += [
    'compass.apps.CompassConfig',
    'simple_history',
    'webpack_loader',
    'supporttools',
    'userservice',
    'compressor',
    'django_user_agents',
]

MIDDLEWARE += ['userservice.user.UserServiceMiddleware',
               'django_user_agents.middleware.UserAgentMiddleware']

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
        'django.template.context_processors.request',
        'supporttools.context_processors.supportools_globals',
        'supporttools.context_processors.has_less_compiled',
    ]
)

# Support tools
SUPPORTTOOLS_PARENT_APP = "compass"
SUPPORTTOOLS_PARENT_APP_URL = "/"

if os.getenv("ENV") == "localdev":
    DEBUG = True
    COMPASS_USERS_GROUP = "u_test_group"
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
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['jadviser'],
        'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
        'eppn': ['jadviser@uw.edu'],
        'scopedAffiliations': ['student@washington.edu',
                               'member@washington.edu'],
        'isMemberOf': ['u_test_group', 'u_astra_compass_omad'],
    }
else:
    COMPASS_USERS_GROUP = os.getenv('ACCESS_GROUP', '')
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, '/static/webpack-stats.json'),
        }
    }
