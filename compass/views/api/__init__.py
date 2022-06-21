# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.decorators import verify_access
from compass.models import AccessGroup
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from uw_saml.utils import get_attribute


@method_decorator(verify_access(), name='dispatch')
class BaseAPIView(GenericAPIView):

    def get_access_groups(self, request):
        groups = get_attribute(request, 'isMemberOf') or []
        access_groups = AccessGroup.objects.filter(access_group_id__in=groups)
        return access_groups
