# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from uw_saml.decorators import group_required
from uw_person_client import UWPersonClient


@method_decorator(group_required(settings.COMPASS_USERS_GROUP),
                  name='dispatch')
class AdviserListView(View):
    '''
    API endpoint returning a list of advisers

    /api/internal/adviser/
    '''
    def get(self, request, *args, **kwargs):
        client = UWPersonClient()
        data = client.get_advisers()
        return JsonResponse([item.to_dict() for item in data], safe=False)
