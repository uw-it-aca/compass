# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from uw_person_client import UWPersonClient


@method_decorator(verify_access(), name='dispatch')
class AdviserListView(View):
    '''
    API endpoint returning a list of advisers

    /api/internal/adviser/
    '''
    def get(self, request, *args, **kwargs):
        client = UWPersonClient()
        data = client.get_advisers()
        return JsonResponse([item.to_dict() for item in data], safe=False)
