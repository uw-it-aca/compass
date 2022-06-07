# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib import admin
from django.urls import re_path
from compass.admin import admin_site
from compass.views.pages import LandingView
from compass.views.api.student import StudentListView, StudentDetailView
from compass.views.api.adviser import AdviserListView
from compass.views.api.contact import ContactListView


urlpatterns = [
    re_path(r'^admin', admin_site.urls),
    re_path(r'^api/internal/student/$',
            StudentListView.as_view()),
    re_path(r'^api/internal/student/(?P<uwnetid>[-@:\w]+)/$',
            StudentDetailView.as_view()),
    re_path(r'^api/internal/student/(?P<systemkey>[-@:\w]+)/contacts/$',
            ContactListView.as_view()),
    re_path(r'^api/internal/adviser/$',
            AdviserListView.as_view()),
    re_path(r"^.*$", LandingView.as_view(), name="index"),
]
