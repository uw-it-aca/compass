# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from compass.admin import admin_site
from django.conf import settings
from django.views.generic import TemplateView
from compass.views.pages import LandingView
from compass.views.api.student import StudentListView, StudentDetailView
from compass.views.api.adviser import AdviserListView
from compass.views.api.contact import ContactListView, ContactTopicsView, \
    ContactTypesView, ContactSaveView, ContactDetailView


# start with an empty url array
urlpatterns = []

# add debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        re_path(
            r"^500$",
            TemplateView.as_view(template_name="500.html"),
            name="500_response",
        ),
        re_path(
            r"^404$",
            TemplateView.as_view(template_name="404.html"),
            name="404_response",
        ),
        re_path(
            r"^403$",
            TemplateView.as_view(template_name="403.html"),
            name="403_response",
        ),
    ]


urlpatterns = [
    re_path(r'^admin', admin_site.urls),
    re_path(r'^api/internal/student/$',
            StudentListView.as_view()),
    re_path(r'^api/internal/student/(?P<uwnetid>[-@:\w]+)/$',
            StudentDetailView.as_view()),
    re_path(r'^api/internal/student/(?P<systemkey>[\w]+)/contacts/$',
            ContactListView.as_view()),
    re_path(r'^api/internal/contact/save/$',
            ContactSaveView.as_view()),
    re_path(r'^api/internal/contact/topics/$',
            ContactTopicsView.as_view()),
    re_path(r'^api/internal/contact/types/$',
            ContactTypesView.as_view()),
    re_path(r'^api/internal/contact/(?P<contactid>[\w]+)/$',
            ContactDetailView.as_view()),
    re_path(r'^api/internal/adviser/$',
            AdviserListView.as_view()),
    # not authorized page that responds as 403
    re_path(
        r"^not-authorized$",
        TemplateView.as_view(template_name="403.html"),
        name="403_response",
    ),
    # vue-router paths
    re_path(r"^(student|caseload|reports|settings)$", LandingView.as_view()),
    # default landing
    re_path(r"^.*$", LandingView.as_view(), name="index"),
]
