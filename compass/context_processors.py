# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.urls import reverse
from userservice.user import UserService
from persistent_message.models import Message
from compass.dao.term import term_context
from compass.models import AccessGroup


def google_analytics(request):
    return {'ga_key': getattr(settings, 'GOOGLE_ANALYTICS_KEY', '')}


def django_debug(request):
    return {'django_debug': getattr(settings, 'DEBUG', False)}


def term(request):
    return term_context()


def auth_user(request):
    us = UserService()
    ret = {
        'user_netid': us.get_original_user(),
        'user_override': us.get_user(),
        'signout_url': reverse('saml_logout'),
        'messages': [],
    }

    try:
        access_group = AccessGroup.objects.access_group_for_user(request)
        ret['user_role'] = AccessGroup.ROLE_MANAGER if (
            access_group.has_manager_role(request)) else AccessGroup.ROLE_USER
    except AccessGroup.DoesNotExist:
        ret['user_role'] = None

    for message in Message.objects.active_messages():
        if 'message_level' not in ret:
            ret['message_level'] = message.get_level_display().lower()
        ret['messages'].append(message.render())

    return ret
