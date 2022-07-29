# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from uw_saml.utils import is_member_of_group


def can_override_user(request):
    return (is_member_of_group(request, settings.COMPASS_SUPPORT_GROUP) or
            is_member_of_group(request, settings.COMPASS_ADMIN_GROUP))


def can_proxy_restclient(request, service, url):
    return (is_member_of_group(request, settings.COMPASS_SUPPORT_GROUP) or
            is_member_of_group(request, settings.COMPASS_ADMIN_GROUP))
