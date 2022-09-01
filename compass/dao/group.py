# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from userservice.user import UserService
from uw_gws import GWS
from uw_saml.utils import is_member_of_group


def is_group_member(request, group_id):
    """
    Check the actual group membership for the logged-in user. If user override
    is active, the membership must be checked using the Groups Web Service,
    otherwise the SAML session will contain the asserted memberships.
    """
    us = UserService()
    if us.get_override_user() is not None:
        return GWS().is_effective_member(group_id, us.get_user())
    else:
        return is_member_of_group(request, group_id)


def is_admin_user(request):
    """
    This check is always a SAML-asserted group membership.
    """
    return is_member_of_group(request, settings.COMPASS_ADMIN_GROUP)


def is_support_user(request):
    """
    This check is always a SAML-asserted group membership.
    """
    return is_member_of_group(request, settings.COMPASS_SUPPORT_GROUP)
