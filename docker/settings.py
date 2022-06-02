from .base_settings import *

INSTALLED_APPS += [
    'compass.apps.CompassConfig',
    'simple_history',
    'webpack_loader',
    'supporttools',
    'userservice',
    'django_user_agents',
]

MIDDLEWARE += ['userservice.user.UserServiceMiddleware',
               'django_user_agents.middleware.UserAgentMiddleware']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                "compass.context_processors.google_analytics",
                "compass.context_processors.logout_url",
                "compass.context_processors.django_debug",
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'supporttools.context_processors.supportools_globals',
                'supporttools.context_processors.has_less_compiled',
            ],
        }
    }
]

# If you have file data, define the path here
DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

if os.getenv("ENV") == "localdev":
    DEBUG = True

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

SUPPORTTOOLS_PARENT_APP = "compass"
SUPPORTTOOLS_PARENT_APP_URL = "/"

# Restclient Configs
APPLICATION_CERT_PATH = os.getenv('CERT_PATH', '')
APPLICATION_KEY_PATH = os.getenv('KEY_PATH', '')
RESTCLIENTS_CA_BUNDLE = '/etc/ssl/certs/ca-certificates.crt'
RESTCLIENTS_DAO_CACHE_CLASS = os.getenv('CACHE_CLASS', '')
RESTCLIENTS_DEFAULT_CONNECT_TIMEOUT = 3
RESTCLIENTS_DEFAULT_TIMEOUT = 10
RESTCLIENTS_DEFAULT_POOL_SIZE = 10
RESTCLIENTS_DEFAULT_ENVS = ['PROD', 'EVAL']

# GWS Config
RESTCLIENTS_GWS_CONNECT_TIMEOUT = os.getenv(
    "GWS_CONNECT_TIMEOUT", RESTCLIENTS_DEFAULT_CONNECT_TIMEOUT)
RESTCLIENTS_GWS_TIMEOUT = os.getenv(
    "GWS_TIMEOUT", RESTCLIENTS_DEFAULT_TIMEOUT)
RESTCLIENTS_GWS_POOL_SIZE = os.getenv(
    "GWS_POOL_SIZE", RESTCLIENTS_DEFAULT_POOL_SIZE)
RESTCLIENTS_GWS_CERT_FILE = APPLICATION_CERT_PATH
RESTCLIENTS_GWS_KEY_FILE = APPLICATION_KEY_PATH
if os.getenv('GWS_ENV') == 'PROD':
    RESTCLIENTS_GWS_DAO_CLASS = 'Live'
    RESTCLIENTS_GWS_HOST = 'https://groups.uw.edu'
elif os.getenv('GWS_ENV') == 'EVAL':
    RESTCLIENTS_GWS_DAO_CLASS = 'Live'
    RESTCLIENTS_GWS_HOST = 'https://iam-ws.u.washington.edu:7443'
else:
    RESTCLIENTS_GWS_DAO_CLASS = 'Mock'
