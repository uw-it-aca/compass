# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import re_path
from compass.admin import admin_site
from django.conf import settings
from django.views.generic import TemplateView
from compass.views.pages import LandingView
from compass.views.admin.contact import OMADContactAdminView
from compass.views.api.student import (
    StudentContactsView,
    StudentSchedulesView,
    StudentTranscriptsView,
    StudentAffiliationsView,
    StudentVisitsView,
    StudentEligibilityView,
    StudentView,
)
from compass.views.api.eligibility import EligibilityView
from compass.views.api.special_program import SpecialProgramView
from compass.views.api.access_group import AccessGroupView
from compass.views.api.adviser import AdviserCheckInsView, AdviserCaseloadView
from compass.views.api.contact import (
    ContactTopicsView,
    ContactTypesView,
    ContactMethodsView,
    ContactView,
    ContactOMADView
)
from compass.views.api.visit import VisitOMADView
from compass.views.api.settings import SettingsView
from compass.views.api.photo import PhotoView
from compass.views.api.affiliation import AffiliationsView
from compass.views.api.support import SupportView
from compass.views.api.user_prefs import UserPreferenceView

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

urlpatterns += [
    re_path(r"^robots\.txt$", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
    re_path(r"^admin", admin_site.urls),
    re_path(
        r"^unauthorized-user$",
        TemplateView.as_view(template_name="unauthorized-user.html"),
        name="unauthorized_user",
    ),
    re_path(
        r"^api/internal/student/(?P<identifier>[-@:\w]+)/$",
        StudentView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<uwregid>[a-fA-F0-9]{32})/schedules/$",
        StudentSchedulesView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<uwregid>[a-fA-F0-9]{32})/transcripts/$",
        StudentTranscriptsView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)/contacts/$",
        StudentContactsView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)/affiliations/$",
        StudentAffiliationsView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)"
        r"/affiliations/(?P<affiliation_id>[\w]+)/$",
        StudentAffiliationsView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)/visits/$",
        StudentVisitsView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)/eligibility/$",
        StudentEligibilityView.as_view(),
    ),
    re_path(
        r"^api/internal/student/(?P<systemkey>[\w]+)/special_program/$",
        SpecialProgramView.as_view(),
        name="special_program_view"
    ),
    re_path(
        r"^api/internal/eligibility/",
        EligibilityView.as_view(),
        name="eligibility_view"
    ),
    re_path(
        r"^api/internal/accessgroup/(?P<access_group_id>[\w]+)/settings/"
        r"(?P<setting_type>[\w]+)/$",
        SettingsView.as_view(),
    ),
    re_path((r"^api/internal/accessgroup/affiliations/$"),
            AffiliationsView.as_view()),
    re_path(r"^api/internal/accessgroup/$",
            AccessGroupView.as_view(),
            name="access_group_view"),
    re_path(r"^api/internal/contact/topics/$", ContactTopicsView.as_view()),
    re_path(r"^api/internal/contact/types/$", ContactTypesView.as_view()),
    re_path(r"^api/internal/contact/methods/$", ContactMethodsView.as_view()),
    re_path(r"^api/internal/contact/(?P<contactid>[\w]+)/$",
            ContactView.as_view(),
            name="contact_edit_view"),
    re_path(r"^api/internal/contact/$",
            ContactView.as_view(),
            name="contact_create_view"),
    re_path(r"^api/internal/contact/$",  ContactView.as_view()),
    re_path(
        r"^api/internal/adviser/(?P<adviser_netid>[\w]+)/checkins/$",
        AdviserCheckInsView.as_view(),
        name="adviser_checkins"
    ),
    re_path(
        r"^api/internal/adviser/(?P<adviser_netid>[\w]+)/caseload/$",
        AdviserCaseloadView.as_view(),
    ),
    re_path(
        r"^api/internal/photo/(?P<uwregid>[a-fA-F0-9]{32})/"
        r"(?P<photo_key>[a-z0-9]{16})/$",
        PhotoView.as_view(),
        name="photo",
    ),
    re_path(
        r"^api/internal/support/omad_contact/$",
        OMADContactAdminView.as_view(),
        name="omad_contact_admin",
    ),
    re_path(
        r"^api/internal/support/$",
        SupportView.as_view(),
    ),
    re_path(
        r"^api/internal/userprefs/$",
        UserPreferenceView.as_view(),
        name="user_preference_view",
    ),
    re_path(
        r"^api/v1/contact/omad/$",
        ContactOMADView.as_view(),
        name="contact_omad"
    ),
    re_path(
        r"^api/v1/visit/omad",
        VisitOMADView.as_view(),
        name="visit_omad"
    ),
    # vue-router paths
    re_path(r"^(checkins|student|caseload|reports).*$", LandingView.as_view()),
    # default landing
    re_path(r"^$", LandingView.as_view(), name="index"),
]
