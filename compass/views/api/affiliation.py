# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import AccessGroup, Affiliation
from compass.serializers import AffiliationSerializer
from compass.views.api import BaseAPIView


class AffiliationsView(BaseAPIView):
    '''
    API endpoint returning a list of affiliations for the user's access group

    /api/internal/accessgroup/affiliations/
    '''

    def get(self, request):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        affiliations = Affiliation.objects.filter(
            access_group=access_group).filter(active=True).all()
        serializer = AffiliationSerializer(affiliations, many=True)
        return self.response_ok(serializer.data)
