# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import TokenAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from compass.dao.rad_csv import validate_prediction_csv


@method_decorator(csrf_exempt, name='dispatch')
class PredictionAnalytics(TokenAPIView):
    def post(self, request, *args, **kwargs):
        """
        Endpoint to accept prediction analytics CSV
        Sample payload:
        ,system_key,student_no,uw_netid,yrq,course_code,pred
        0,0000001,8123456,javerage  ,20252,TRAIN 100 A,False
        1,0000002,1000002,jsmith    ,20252,BIOL 101 A,True
        """
        # validate payload
        body = request.body.decode('utf-8')
        try:
            validate_prediction_csv(body)
        except ValueError as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)

        #
        # try:
        #     validate_contact_post_data(contact_dict)
        # except AccessGroup.DoesNotExist as e:
        #     return Response(repr(e), status=status.HTTP_501_NOT_IMPLEMENTED)
        # except ValueError as e:
        #     return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)
        # except PersonNotFoundException as e:
        #     return Response("Person record for adviser not found",
        #                     status=status.HTTP_400_BAD_REQUEST)
