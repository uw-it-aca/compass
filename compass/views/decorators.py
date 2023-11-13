# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from uw_saml.utils import get_user
from compass.dao.person import person_from_uwnetid, PersonNotFoundException
from logging import getLogger

logger = getLogger(__name__)


def xhr_login_required(view_func):
    """
    A login_required decorator for API views that handle
    asynchronous requests.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        requested_with = request.META.get('HTTP_X_REQUESTED_WITH', '')
        if requested_with == 'XMLHttpRequest':
            return HttpResponse(content='Invalid session', status=403)

        return redirect_to_login(request.path)

    return wrapper


def person_required(view_func):
    """
    A decorator for views that checks whether the login is a personal
    identity with a valid affiliation.  Calls login_required if the user
    is not authenticated.
    """
    def wrapper(request, *args, **kwargs):
        try:
            username = get_user(request)
            kwargs['person'] = person_from_uwnetid(username)
            return view_func(request, *args, **kwargs)
        except PersonNotFoundException:
            logger.info(f"Nonpersonal or unknown login blocked: {username}")
            return HttpResponseRedirect(reverse('unauthorized_user'))

    return login_required(function=wrapper)
