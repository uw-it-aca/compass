# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.models import AccessGroup, EligibilityType
from compass.serializers import EligibilityTypeSerializer


class EligibilityView(BaseAPIView):
    '''
    API endpoint for eligibility information

    /api/internal/eligibility
    '''
    def get(self, request):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        eligibilities = []
        for e in EligibilityType.objects.filter(access_group=access_group):
            eligibilities.append(EligibilityTypeSerializer(e, many=False).data)

        return self.response_ok(eligibilities)
