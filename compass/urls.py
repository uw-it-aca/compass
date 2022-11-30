# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path, include
from compass.admin import admin_site
from django.conf import settings
from django.views.generic import TemplateView
from compass.views.pages import LandingView
from compass.views.api.student import (
    StudentContactsView,
    StudentSchedulesView,
    StudentTranscriptsView,
    StudentView,
)
from compass.views.api.access_group import AccessGroupView
from compass.views.api.adviser import AdviserContactsView, AdviserCaseloadView
from compass.views.api.contact import (
    ContactTopicsView,
    ContactTypesView,
    ContactMethodsView,
    ContactView,
    ContactOMADView
)
from compass.views.api.settings import SettingsView
from compass.views.api.photo import PhotoView
from compass.views.api.program import ProgramsView
from compass.views.api.support import SupportView

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
        re_path(
            r"^unauthorized-user$",
            TemplateView.as_view(template_name="unauthorized-user.html")
        ),
    ]

urlpatterns += [
    re_path(r"^admin", admin_site.urls),
    re_path(
        r"^api/internal/student/(?P<student_identifier>[-@:\w]+)/$",
        StudentView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<uwregid>[-@:\w]+)/schedules/$",
        StudentSchedulesView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<uwregid>[-@:\w]+)/transcripts/$",
        StudentTranscriptsView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)/contacts/$",
        StudentContactsView.as_view(),
    ),
    re_path(
        r"^api/internal/accessgroup/(?P<access_group_pk>[\w]+)/settings/"
        r"(?P<setting_type>[\w]+)/$",
        SettingsView.as_view(),
    ),
    re_path(r"^api/internal/accessgroup/(?P<access_group_pk>[\w]+)/programs/$",
            ProgramsView.as_view()),
    re_path(r"^api/internal/accessgroup/$", AccessGroupView.as_view()),
    re_path(r"^api/internal/contact/topics/$", ContactTopicsView.as_view()),
    re_path(r"^api/internal/contact/types/$", ContactTypesView.as_view()),
    re_path(r"^api/internal/contact/methods/$", ContactMethodsView.as_view()),
    re_path(r"^api/internal/contact/(?P<contactid>[\w]+)/$",
            ContactView.as_view()),
    re_path(r"^api/internal/contact/$",  ContactView.as_view()),
    re_path(
        r"^api/internal/adviser/(?P<adviser_netid>[\w]+)/contacts/$",
        AdviserContactsView.as_view(),
    ),
    re_path(
        r"^api/internal/adviser/(?P<adviser_netid>[\w]+)/caseload/$",
        AdviserCaseloadView.as_view(),
    ),
    re_path(
        r"^api/internal/photo/(?P<photo_key>[a-z0-9]*)/$",
        PhotoView.as_view(),
        name="photo",
    ),
    re_path(
        r"^api/internal/support/$",
        SupportView.as_view(),
    ),
    re_path(
        r"^api/v1/contact/omad/$",
        ContactOMADView.as_view(),
        name="contact_omad"
    ),
    # vue-router paths
    re_path(r"^(student|caseload|reports|settings).*$", LandingView.as_view()),
    re_path(r'^saml/', include('uw_saml.urls')),
    # default landing
    re_path(r"^$", LandingView.as_view(), name="index"),
]
