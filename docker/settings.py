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

TEMPLATES[0]['OPTIONS']['context_processors'].extend([
    'compass.context_processors.google_analytics',
    'compass.context_processors.django_debug'
])

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

if os.getenv("ENV") == "localdev":
    DEBUG = True
    COMPASS_USERS_GROUP = 'u_test_group'
else:
    COMPASS_USERS_GROUP = os.getenv('ACCESS_GROUP', '')

ENROLLMENT_STATUS_MAPPING = {
    12: "REGISTERED",
    81: "CANCL-NSF CK",
    82: "CANCL-REGIST",
    83: "CANCL-LOW SC",
    84: "CANCL-HFS",
    85: "CANCL-NONPAY",
    86: "CANCL-SC LN",
    90: "MIL BEF 9TH",
    92: "MIL 2ND 1/3",
    93: "MIL LAST 1/3",
    95: "WTHDR BEF QT",
    96: "WITHDRAWAL"
}
