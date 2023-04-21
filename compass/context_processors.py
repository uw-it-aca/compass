# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.urls import reverse
from userservice.user import UserService
from compass.dao.term import term_context
from compass.models import AccessGroup


def google_analytics(request):
    return {'ga_key': getattr(settings, 'GOOGLE_ANALYTICS_KEY', '')}


def django_debug(request):
    return {'django_debug': getattr(settings, 'DEBUG', False)}


def term_context(request):
    return term_context()


def auth_user(request):
    us = UserService()
    roles = AccessGroup.objects.get_roles_for_user(request)
    return {
        'user_netid': us.get_original_user(),
        'user_override': us.get_user(),
        'user_role': ','.join(sorted(roles)),
        'signout_url': reverse('saml_logout'),
    }
