# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.views.api import TokenAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from compass.dao.rad_csv import validate_prediction_csv
from compass.dao.storage import RADStorageDao


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
        if settings.PRED_ANALYTICS_TOKEN_USER != request.user.username:
            return Response("Unauthorized",
                            status=status.HTTP_401_UNAUTHORIZED)
        # validate payload
        body = request.body.decode('utf-8')
        try:
            validate_prediction_csv(body)
        except ValueError as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)
        RADStorageDao().write_pred_file(body)
        return Response(status=status.HTTP_201_CREATED)
