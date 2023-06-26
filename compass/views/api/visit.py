# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView
from compass.models import Visit, VisitTopic, Student
from compass.serializers import VisitReadSerializer, VisitTypeSerializer


class VisitView(BaseAPIView):
    '''
    API endpoint for visit

    /api/internal/visit/(visitid)/
    '''
    def get(self, request, visitid):
        try:
            visit = Visit.objects.get(id=visitid)
        except Visit.DoesNotExist:
            return self.response_notfound()

        serializer = VisitReadSerializer(visit, many=False)
        return self.response_ok(serializer.data)
