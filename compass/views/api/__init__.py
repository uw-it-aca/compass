# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import AccessGroup, AppUser
from compass.views.decorators import xhr_login_required
from compass.exceptions import OverrideNotPermitted
from django.conf import settings
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from userservice.user import UserService
from logging import getLogger

logger = getLogger(__name__)


@method_decorator(xhr_login_required, name='dispatch')
class BaseAPIView(GenericAPIView):

    def valid_user_override(self):
        if (not getattr(settings, "ALLOW_USER_OVERRIDE_FOR_WRITE", False) and
                UserService().get_override_user() is not None):
            raise OverrideNotPermitted()

    def get_access_group(self, request, require_manager=False):
        access_group, role = AccessGroup.objects.access_group_for_user(
            request, require_manager=require_manager)
        return access_group

    def valid_access_group(self,
                           request,
                           access_groups,
                           require_manager=False):
        user_ag = self.get_access_group(request, require_manager)
        if user_ag not in access_groups:
            raise PermissionDenied()

    def valid_user_permission(self, request,
                              access_groups=None,
                              allow_override=True,
                              require_manager=False):
        try:
            # Check if the user has an access group
            self.get_access_group(request, require_manager)
            # Check if user in list of supplied access groups
            if access_groups:
                self.valid_access_group(request, access_groups,
                                        require_manager=require_manager)
            # Check if override is allowed for action
            if not allow_override:
                self.valid_user_override()
        except (PermissionDenied,
                AccessGroup.DoesNotExist,
                OverrideNotPermitted):
            raise PermissionDenied()

    def get_app_user(self):
        try:
            us = UserService()
            return AppUser.objects.get(uwnetid=us.get_user())
        except AppUser.DoesNotExist:
            raise PermissionDenied()

    def response_ok(self, content):
        return Response(content, status=status.HTTP_200_OK)

    def response_created(self, content):
        return Response(content, status=status.HTTP_201_CREATED)

    def response_accepted(self, content):
        return Response(content, status=status.HTTP_202_ACCEPTED)

    def response_badrequest(self, content="Missing parameters"):
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def response_unauthorized(self, content="Not authorized"):
        # content may be an Exception object
        if isinstance(content, BaseException):
            content = str(content)
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def response_notfound(self, content="Not found"):
        return Response(content, status=status.HTTP_404_NOT_FOUND)


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
