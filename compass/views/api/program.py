# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import Program
from compass.serializers import ProgramSerializer
from compass.views.api import BaseAPIView
from rest_framework.response import Response
from rest_framework import status


class ProgramsView(BaseAPIView):
    '''
    API endpoint returning a list of programs for the user's access group

    /api/internal/accessgroup/[access_group_pk]/programs/
    '''

    def get(self, request, access_group_pk):
        programs = Program.objects.filter(
            access_group=access_group_pk).filter(active=True).all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
