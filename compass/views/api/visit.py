# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView, JSONClientContentNegotiation, \
    TokenAPIView
from compass.models import AccessGroup, Visit, VisitTopic, Student
from compass.serializers import VisitReadSerializer, VisitTypeSerializer
from dateutil import parser
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


class VisitView(BaseAPIView):
    '''
    API endpoint for visit

    /api/internal/visit/(visitid)/
    '''
    def get(self, request, visitid):
        visit = Visit.objects.filter(id=visitid).get()
        access_groups = self.get_access_groups(request)
        if any(app_user_group in visit.access_group.all() for
               app_user_group in access_groups):
            serializer = VisitReadSerializer(visit, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(f"User not authorized to access visit "
                            f"{visitid}",
                            status=status.HTTP_401_UNAUTHORIZED)
