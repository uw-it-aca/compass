# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import include, re_path
from compass.views.pages import LandingView
from compass.views.api.photo import PhotoView
from compass.views.api.student import StudentListView, StudentDetailView


urlpatterns = [
    re_path(r'^api/internal/photo/(?P<photo_key>[a-z0-9]*)/$',
            PhotoView.as_view(), name='photo'),
    re_path(r'^api/internal/student/$',
            StudentListView.as_view(), name='student_detail'),
    re_path(r'^api/internal/student/(?P<student_number>[-@:\w]+)/$',
            StudentDetailView.as_view(), name='student_list'),
    re_path(r"^.*$", LandingView.as_view(), name="index"),
]
