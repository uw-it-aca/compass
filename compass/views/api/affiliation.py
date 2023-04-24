# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import Affiliation
from compass.serializers import AffiliationSerializer
from compass.views.api import BaseAPIView
from rest_framework.response import Response
from rest_framework import status


class AffiliationsView(BaseAPIView):
    '''
    API endpoint returning a list of affiliations for the user's access group

    /api/internal/accessgroup/[access_group_pk]/affiliations/
    '''

    def get(self, request, access_group_pk):
        affiliations = Affiliation.objects.filter(
            access_group=access_group_pk).filter(active=True).all()
        serializer = AffiliationSerializer(affiliations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
