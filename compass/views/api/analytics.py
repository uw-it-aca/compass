# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response

from compass.dao.rad_csv import validate_prediction_json
from compass.dao.storage import RADStorageDao
from compass.views.api import TokenAPIView


@method_decorator(csrf_exempt, name='dispatch')
class PredictionAnalytics(TokenAPIView):
    def post(self, request, *args, **kwargs):
        """
        Endpoint to accept prediction analytics JSON
        Sample payload:
        {
            "body": [
                {
                    "": "0",
                    "system_key": "12345",
                    "student_no": "54321",
                    "uw_netid": "netid123",
                    "yrq": "20261",
                    "course_code": "MATH 101 A",
                    "pred": "False"
                },

            ]
        }
        """
        if settings.PRED_ANALYTICS_TOKEN_USER != request.user.username:
            return Response("Unauthorized",
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            validate_prediction_json(request.data)
        except ValueError as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)
        RADStorageDao().write_pred_file(request.data)
        return Response(status=status.HTTP_201_CREATED)
