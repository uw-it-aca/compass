# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from compass.models import AppUser, UserPreference


def get_user_preferences(netid):
    try:
        app_user = AppUser.objects.get(uwnetid=netid)
        user_prefs = UserPreference.objects.filter(app_user=app_user)
        prefs = {}
        for pref in user_prefs:
            if pref.component not in prefs:
                prefs[pref.component] = {}
            prefs[pref.component][pref.key] = pref.value
        return prefs
    except (AppUser.DoesNotExist, UserPreference.DoesNotExist, Exception):
        return None
