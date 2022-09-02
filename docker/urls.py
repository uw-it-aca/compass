from .base_urls import *
from django.urls import re_path, include

urlpatterns += [
    re_path(r'^', include('compass.urls')),
    re_path(r'^support/?', include('userservice.urls')),
    re_path(r'^restclients/', include('rc_django.urls')),
]
