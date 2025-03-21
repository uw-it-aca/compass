# Copyright 2025 UW-IT, University of Washington
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
            invalid_keys = UserPreference.update_by_user_component(app_user,
                                                                   user_prefs)
            if invalid_keys:
                return self.response_accepted("Some keys were not accepted: " +
                                              ", ".join(invalid_keys))
            return self.response_ok("Preferences set")
        except OverrideNotPermitted:
            return self.response_unauthorized()
        except Exception as ex:
            return self.response_badrequest(str(ex))
