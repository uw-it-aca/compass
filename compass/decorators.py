# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import AccessGroup
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from userservice.user import UserService
from uw_gws import GWS
from uw_saml.utils import is_member_of_group


def verify_access():
    """
    A decorator for views that checks uw-saml for whether the user is a member
    of the admin and support groups, as well as the gws for memberships of
    astra groups. Calls login_required if the user is not authenticated.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if UserService().get_override_user() is None:
                # check saml for admin and support group memberships
                if (is_member_of_group(request,
                                       settings.COMPASS_ADMIN_GROUP) or
                    is_member_of_group(request,
                                       settings.COMPASS_SUPPORT_GROUP)):
                    return view_func(request, *args, **kwargs)

            for group_id in AccessGroup.objects.access_group_ids:
                # check the gws for astra group memberships
                if GWS().is_effective_member(group_id,
                                             UserService().get_user()):
                    return view_func(request, *args, **kwargs)

            return render(request,
                          'uw_saml/access_denied.html',
                          status=401)

        return login_required(function=wrapper)

    return decorator
