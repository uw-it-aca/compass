# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.serializers import AccessGroupSerializer
from compass.views.api import BaseAPIView
from rest_framework.response import Response
from rest_framework import status


class AccessGroupView(BaseAPIView):
    '''
    API endpoint returning the list of groups that a user can access

    /api/internal/accessgroup/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)
        serializer = AccessGroupSerializer(access_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
