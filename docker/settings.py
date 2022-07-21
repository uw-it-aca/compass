from .base_settings import *

INSTALLED_APPS += [
    'compass.apps.CompassConfig',
    'simple_history',
    'webpack_loader',
    'userservice',
]

# Location of stats file that can be accessed during local development and
# collected from during production build process
if os.getenv("ENV") == "localdev":
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, 'compass/static/webpack-stats.json'),
        }
    }
else:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, '/static/webpack-stats.json'),
        }
    }

MIDDLEWARE += ['userservice.user.UserServiceMiddleware']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                "compass.context_processors.google_analytics",
                "compass.context_processors.django_debug",
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }
]

# If you have file data, define the path here
DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

if os.getenv("ENV") == "localdev":
    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.join(BASE_DIR, "compass"),
                                 'db.sqlite3'),
        }
    }
    TEST_ACCESS_GROUP = 'u_test_group'
    COMPASS_ADMIN_GROUP = TEST_ACCESS_GROUP
    COMPASS_SUPPORT_GROUP = TEST_ACCESS_GROUP
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['jadviser'],
        'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
        'eppn': ['jadviser@uw.edu'],
        'scopedAffiliations': ['student@washington.edu',
                               'member@washington.edu'],
        'isMemberOf': [TEST_ACCESS_GROUP, 'u_astra_group1'],
    }
else:
    COMPASS_ADMIN_GROUP = os.getenv('ADMIN_GROUP', '')
    COMPASS_SUPPORT_GROUP = os.getenv('SUPPORT_GROUP', '')
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, '/static/webpack-stats.json'),
        }
    }

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default="")
