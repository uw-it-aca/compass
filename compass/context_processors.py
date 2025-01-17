# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.urls import reverse
from userservice.user import UserService
from restclients_core.exceptions import DataFailureException
from persistent_message.models import Message
from compass.dao.term import term_context
from compass.dao import current_datetime
from compass.models import AccessGroup
from compass.dao.preferences import get_user_preferences


def google_analytics(request):
    return {'ga_key': getattr(settings, 'GOOGLE_ANALYTICS_KEY', '')}


def django_debug(request):
    return {'django_debug': getattr(settings, 'DEBUG', False)}


def auth_user(request):
    us = UserService()
    ret = {
        'user_netid': us.get_original_user(),
        'user_override': us.get_user(),
        'user_role': None,
        'signout_url': reverse('saml_logout'),
        'messages': [],
    }

    try:
        access_group, role = AccessGroup.objects.access_group_for_user(request)
        ret['user_role'] = role
        ret['user_access_group'] = access_group.access_group_id
    except DataFailureException:
        ret['messages'].append(
            'The UW Groups Service is currently unavailable.')
    except AccessGroup.DoesNotExist:
        pass

    try:
        ret.update(term_context())
    except DataFailureException:
        ret['current_date'] = current_datetime().date().isoformat()
        ret['messages'].append(
            'The Student Web Service is currently unavailable.')

    for message in Message.objects.active_messages():
        if 'message_level' not in ret:
            ret['message_level'] = message.get_level_display().lower()
        ret['messages'].append(message.render())

    return ret


def user_preferences(request):
    us = UserService()
    netid = us.get_user()
    user_prefs = get_user_preferences(netid)
    return {'user_preferences': user_prefs if user_prefs else {}}
