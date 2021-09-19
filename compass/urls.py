# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, re_path
from compass.views.pages import HomeView
from compass.views.api.student import StudentListView, StudentDetailView


urlpatterns = [
    re_path(r'^api/internal/student/list/$',
            StudentListView.as_view()),
    re_path(r'^api/internal/student/list/$',
            StudentDetailView.as_view()),
    re_path(r"^$", HomeView.as_view(), name="index"),
]
