# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import AccessGroup
from compass.serializers import AccessGroupSerializer
from compass.views.api import BaseAPIView


class AccessGroupView(BaseAPIView):
    '''
    API endpoint returning the list of groups that a user can access

    /api/internal/accessgroup/
    '''

    def get(self, request):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        serializer = AccessGroupSerializer([access_group], many=True)
        return self.response_ok(serializer.data)
