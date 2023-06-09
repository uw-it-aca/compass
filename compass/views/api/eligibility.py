# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.models import EligibilityType
from compass.serializers import EligibilityTypeSerializer
from rest_framework.response import Response
from rest_framework import status


class EligibilityView(BaseAPIView):
    '''
    API endpoint for eligibility information

    /api/internal/eligibility
    '''
    def get(self, request):
        eligibilities = []
        access_groups = self.get_access_groups(request)
        for e in EligibilityType.objects.filter(
                access_group__in=access_groups):
            eligibilities.append(EligibilityTypeSerializer(e, many=False).data)

        return Response(eligibilities, status=status.HTTP_200_OK)
