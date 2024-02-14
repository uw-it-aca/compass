# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import (
    BaseAPIView)
from compass.models import (AppUser, UserPreference)
from userservice.user import UserService
from compass.exceptions import OverrideNotPermitted


class UserPreferenceView(BaseAPIView):
    """
    Handles creating and updating user preferences
    """
    def put(self, request):
        try:
            self.valid_user_override()
            us = UserService()
            app_user = AppUser.objects.upsert_appuser(us.get_user())
            user_prefs = request.data
            invalid_keys = []
            for component, prefs in user_prefs.items():
                for key, value in prefs.items():
                    if UserPreference.validate_preference(component, key):
                        UserPreference.objects.update_or_create(
                            app_user=app_user,
                            component=component,
                            key=key,
                            defaults={'value': value})
                    else:
                        invalid_keys.append(f"{component}.{key}")
            if invalid_keys:
                return self.response_accepted("Some keys were not accepted: " +
                                              ", ".join(invalid_keys))
            return self.response_ok("Preferences set")
        except OverrideNotPermitted:
            return self.response_unauthorized()
        except Exception as ex:
            return self.response_badrequest(str(ex))
