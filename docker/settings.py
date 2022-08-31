from .base_settings import *

INSTALLED_APPS += [
    'compass.apps.CompassConfig',
    'django_user_agents',
    'simple_history',
    'supporttools',
    'userservice',
]

if os.getenv("ENV") == "localdev":
    DEBUG = True

if os.getenv("ENV") == "localdev":
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "compass", "static", "manifest.json"
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", "manifest.json")


MIDDLEWARE += [
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

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
        'isMemberOf': [TEST_ACCESS_GROUP, 'u_astra_group1-manager'],
    }
else:
    COMPASS_ADMIN_GROUP = os.getenv('ADMIN_GROUP', '')
    COMPASS_SUPPORT_GROUP = os.getenv('SUPPORT_GROUP', '')

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default="")

# Where the back link should go, and how it's labeled.
SUPPORTTOOLS_PARENT_APP = "Compass"
SUPPORTTOOLS_PARENT_APP_URL = "/"

USERSERVICE_VALIDATION_MODULE = 'compass.dao.person.is_netid'
USERSERVICE_OVERRIDE_AUTH_MODULE = 'compass.views.can_override_user'
RESTCLIENTS_ADMIN_AUTH_MODULE = 'compass.views.can_proxy_restclient'

# PDS config
AXDD_PERSON_CLIENT_ENV = os.getenv('AXDD_PERSON_CLIENT_ENV', '')
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME', '')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD', '')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', '')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', '')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '')
