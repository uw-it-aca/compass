from .base_settings import *

INSTALLED_APPS += [
    'compass.apps.CompassConfig',
    'django_user_agents',
    'simple_history',
    'supporttools',
    'rc_django',
    'userservice',
    'persistent_message',
    'rest_framework',
    'rest_framework.authtoken'
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'supporttools.context_processors.supportools_globals',
                'supporttools.context_processors.has_less_compiled',
                'compass.context_processors.google_analytics',
                'compass.context_processors.django_debug',
                'compass.context_processors.auth_user',
            ],
        }
    }
]

# If you have file data, define the path here
DATA_ROOT = os.path.join(BASE_DIR, "compass/data")

if os.getenv("ENV") == "localdev":
    DEBUG = True
    RESTCLIENTS_DAO_CACHE_CLASS = None
    CURRENT_DATETIME_OVERRIDE = "2020-10-15 00:00:00"

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
    RESTCLIENTS_DAO_CACHE_CLASS = 'compass.cache.CompassRestclientCache'
    COMPASS_ADMIN_GROUP = os.getenv('ADMIN_GROUP', '')
    COMPASS_SUPPORT_GROUP = os.getenv('SUPPORT_GROUP', '')

    # Django cache backend for the idcard tokens
    CACHES = {
        'default': {
            'BACKEND': 'memcached_clients.django_backend.PymemcacheCache',
            'LOCATION': MEMCACHED_SERVERS,
            'OPTIONS': {
                'use_pooling': MEMCACHED_USE_POOLING,
                'max_pool_size': MEMCACHED_MAX_POOL_SIZE,
            }
        }
    }
    CSRF_TRUSTED_ORIGINS = ['https://' + os.getenv('CLUSTER_CNAME')]

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default="")

# Where the back link should go, and how it's labeled.
SUPPORTTOOLS_PARENT_APP = "Compass"
SUPPORTTOOLS_PARENT_APP_URL = "/"

USERSERVICE_VALIDATION_MODULE = 'compass.dao.person.is_overridable_uwnetid'
USERSERVICE_OVERRIDE_AUTH_MODULE = 'compass.dao.group.can_override_user'
RESTCLIENTS_ADMIN_AUTH_MODULE = 'compass.dao.group.can_proxy_restclient'
PERSISTENT_MESSAGE_AUTH_MODULE = 'compass.dao.group.can_manage_persistent_messages'
ALLOW_USER_OVERRIDE_FOR_WRITE = (os.getenv('ENV', 'localdev') != 'prod')

# IDCard photo config
IDCARD_TOKEN_EXPIRES = 60 * 60

# PDS config
UW_PERSON_DB_USERNAME = os.getenv('UW_PERSON_DB_USERNAME', '')
UW_PERSON_DB_PASSWORD = os.getenv('UW_PERSON_DB_PASSWORD', '')
UW_PERSON_DB_HOSTNAME = os.getenv('UW_PERSON_DB_HOSTNAME', '')
UW_PERSON_DB_DATABASE = os.getenv('UW_PERSON_DB_DATABASE', '')
UW_PERSON_DB_PORT = os.getenv('UW_PERSON_DB_PORT', '')
UW_PERSON_DB_POOL_SIZE = os.getenv('UW_PERSON_DB_POOL_SIZE', 1)
UW_PERSON_DB_MAX_OVERFLOW = os.getenv('UW_PERSON_DB_MAX_OVERFLOW', 2)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'add_user': {
            '()': 'compass.logging.UserFilter'
        },
        'stdout_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno < logging.WARNING
        },
        'stderr_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno > logging.INFO
        }
    },
    'formatters': {
        'compass': {
            'format': '%(levelname)-4s %(asctime)s %(user)s %(actas)s %(message)s [%(name)s]',
            'datefmt': '[%Y-%m-%d %H:%M:%S]',
        },
        'restclients_timing': {
            'format': '%(levelname)-4s restclients_timing %(module)s %(asctime)s %(message)s [%(name)s]',
            'datefmt': '[%Y-%m-%d %H:%M:%S]',
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['add_user', 'stdout_stream'],
            'formatter': 'compass',
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'filters': ['add_user', 'stderr_stream'],
            'formatter': 'compass',
        },
        'restclients_timing': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['stdout_stream'],
            'formatter': 'restclients_timing',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['stderr'],
            'level': 'ERROR',
            'propagate': True,
        },
        'compass': {
            'handlers': ['stdout', 'stderr'],
            'level': 'INFO',
            'propagate': False,
        },
        'restclients_core': {
            'handlers': ['restclients_timing'],
            'level': 'INFO',
            'propagate': False,
        },
        'sqlalchemy.pool': {
            'handlers': ['stdout', 'stderr'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['stdout', 'stderr'],
            'level': 'INFO' if os.getenv('ENV', 'localdev') == 'prod' else 'DEBUG'
        }
    }
}
