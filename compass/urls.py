# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path, include
from compass.admin import admin_site
from compass.views.pages import LandingView
from compass.views.api.student import StudentDetailView, StudentContactsView, \
        StudentSchedulesView, StudentSaveView, StudentTranscriptsView
from compass.views.api.access_group import AccessGroupView
from compass.views.api.adviser import AdviserContactsView, AdviserCaseloadView
from compass.views.api.contact import ContactTopicsView, ContactTypesView, \
    ContactSaveView, ContactDetailView
from compass.views.api.settings import SettingsView
from compass.views.api.photo import PhotoView
from compass.views.api.program import ProgramsView


# start with an empty url array
urlpatterns = []

urlpatterns += [
    re_path(r'^admin', admin_site.urls),
    re_path(r'^support', include('userservice.urls')),
    re_path(r'^api/internal/student/save/$',
            StudentSaveView.as_view()),
    re_path(r'^api/internal/student/(?P<uwnetid>[-@:\w]+)/$',
            StudentDetailView.as_view()),
    re_path(r'^api/internal/student/(?P<uwregid>[-@:\w]+)/schedules/$',
            StudentSchedulesView.as_view()),
    re_path(r'^api/internal/student/(?P<uwregid>[-@:\w]+)/transcripts/$',
            StudentTranscriptsView.as_view()),
    re_path(r'^api/internal/student/(?P<systemkey>[\w]+)/contacts/$',
            StudentContactsView.as_view()),
    re_path(r'^api/internal/settings/(?P<access_group_id>[\w]+)/'
            r'(?P<setting_type>[\w]+)/$',
            SettingsView.as_view()),
    re_path(r'^api/internal/settings/save/$',
            SettingsView.as_view()),
    re_path(r'^api/internal/accessgroup/$',
            AccessGroupView.as_view()),
    re_path(r'^api/internal/programs/$',
            ProgramsView.as_view()),
    re_path(r'^api/internal/contact/save/$',
            ContactSaveView.as_view()),
    re_path(r'^api/internal/contact/topics/$',
            ContactTopicsView.as_view()),
    re_path(r'^api/internal/contact/types/$',
            ContactTypesView.as_view()),
    re_path(r'^api/internal/contact/(?P<contactid>[\w]+)/$',
            ContactDetailView.as_view()),
    re_path(r'^api/internal/adviser/(?P<adviser_netid>[\w]+)/contacts/$',
            AdviserContactsView.as_view()),
    re_path(r'^api/internal/adviser/(?P<adviser_netid>[\w]+)/caseload/$',
            AdviserCaseloadView.as_view()),
    re_path(r'^api/internal/photo/(?P<photo_key>[a-z0-9]*)/$',
            PhotoView.as_view(), name='photo'),
    # vue-router paths
    re_path(r"^(student|caseload|reports|settings)$", LandingView.as_view()),
    # default landing
    re_path(r"^.*$", LandingView.as_view(), name="index"),
]
