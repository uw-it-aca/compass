# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, re_path
from compass.views.pages import PageView
from compass.views.api.edw import EnrolledStudentsListView


urlpatterns = [
    re_path(r'^api/internal/edw/enrolled-students/$',
            EnrolledStudentsListView.as_view()),
    re_path(r"^.*$", PageView.as_view(), name="index"),
]
