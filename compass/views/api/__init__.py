# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import AccessGroup, AppUser
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from uw_saml.utils import get_attribute


@method_decorator(login_required, name='dispatch')
class BaseAPIView(GenericAPIView):

    def get_access_groups(self, request):
        groups = get_attribute(request, 'isMemberOf') or []
        # removed -manager and -user from group name
        groups = [g.rsplit("-", 1)[0] for g in groups]
        access_groups = AccessGroup.objects.filter(access_group_id__in=groups)
        return access_groups

    def get_access_groups_for_user(self, uwnetid):
        try:
            AppUser.objects.upsert_appuser(uwnetid)
        except AppUser.DoesNotExist:
            raise ValueError(f"No error found for uwnetid={uwnetid}")

    def validate_settings_access(self, request, access_group_pk,
                                 roles):
        """
        Raises a PermissionDenied error if the request is not authenticated
        for the specified access group roles.
        """
        access_group = AccessGroup.objects.get(id=access_group_pk)
        for role in roles:
            if not access_group.has_role(request, role):
                raise PermissionDenied()
        return access_group

    def validate_manager_access(self, request, access_group_pk):
        return self.validate_settings_access(request, access_group_pk,
                                             [AccessGroup.ROLE_MANAGER])

    def validate_user_access(self, request, access_group_pk):
        # anything a user can access a manager can also access
        try:
            return self.validate_settings_access(request, access_group_pk,
                                                 [AccessGroup.ROLE_MANAGER])
        except PermissionDenied:
            return self.validate_settings_access(request, access_group_pk,
                                                 [AccessGroup.ROLE_USER])


class TokenAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)


class JSONClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the JSON parser.
        """
        return JSONParser()

    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the JSON renderer.
        """
        renderer = JSONRenderer()
        return renderer, renderer.media_type
