# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import Program
from compass.serializers import ProgramSerializer
from compass.views.api import BaseAPIView
from rest_framework.response import Response
from rest_framework import status


class ProgramsView(BaseAPIView):
    '''
    API endpoint returning a list of programs for the user's access group

    /api/internal/programs/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)
        programs = Program.objects.filter(access_group__in=access_groups).all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
