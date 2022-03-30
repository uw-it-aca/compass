# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, re_path
from compass.views.pages import LandingView
from compass.views.api.student import StudentListView, StudentDetailView


urlpatterns = [
    re_path(r'^api/internal/student/$',
            StudentListView.as_view()),
    re_path(r'^api/internal/student/(?P<student_number>[-@:\w]+)/$',
            StudentDetailView.as_view()),
    re_path(r"^.*$", LandingView.as_view(), name="index"),
]
