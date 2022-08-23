# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import AccessGroup
from django.conf import settings
from userservice.user import UserService
from uw_gws import GWS
from uw_saml.utils import is_member_of_group


class Roles():
    ADMIN = "admin"
    SUPPORT = "support"
    MANAGER = "manager"
    USER = "user"


def is_member_access_group(group_id):
    if (is_access_group_manager(group_id) or
            is_access_group_user(group_id)):
        return True


def is_access_group_manager(group_id):
    return True if GWS().is_effective_member(f"{group_id}-manager",
                                             UserService().get_user()) \
        else False


def is_access_group_user(group_id):
    return True if GWS().is_effective_member(f"{group_id}-user",
                                             UserService().get_user()) \
        else False


def get_user_roles(request):
    roles = set()
    if is_member_of_group(request, settings.COMPASS_ADMIN_GROUP):
        roles.add(Roles.ADMIN)
    if is_member_of_group(request, settings.COMPASS_SUPPORT_GROUP):
        roles.add(Roles.SUPPORT)
    # check the gws for astra group memberships
    for group_id in AccessGroup.objects.access_group_ids:
        if is_access_group_manager(group_id):
            roles.add(roles.Manager)
        if is_access_group_user(group_id):
            roles.add(roles.User)
    return list(roles)
