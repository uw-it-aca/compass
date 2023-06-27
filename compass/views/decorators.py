# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from userservice.user import UserService
from compass.dao.person import person_from_uwnetid, PersonNotFoundException


def uw_person_required():
    """
    A decorator for views that checks whether the login is a UW personal
    UWNetID.  Calls login_required if the user is not authenticated.
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                person = person_from_uwnetid(UserService().get_user())
                return view_func(request, *args, **kwargs)
            except PersonNotFoundException:
                return render(request, 'unauthorized-user.html', status=401)

        return login_required(function=wrapper)

    return decorator
