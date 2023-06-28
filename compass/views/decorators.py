# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from uw_saml.utils import get_user
from compass.dao.person import person_from_uwnetid, PersonNotFoundException
from logging import getLogger

logger = getLogger(__name__)


def uw_person_required(view_func):
    """
    A decorator for views that checks whether the login is a UW personal
    UWNetID.  Calls login_required if the user is not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        try:
            username = get_user(request)
            kwargs['person'] = person_from_uwnetid(username)
            return view_func(request, *args, **kwargs)
        except PersonNotFoundException:
            logger.info(f"Nonpersonal or unknown login blocked: {username}")
            return redirect(reverse('unauthorized_user'))

    return login_required(function=wrapper)
