# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import AccessGroup, AppUser
from compass.exceptions import OverrideNotPermitted
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from userservice.user import UserService


@method_decorator(login_required, name='dispatch')
class BaseAPIView(GenericAPIView):

    def valid_user_override(self):
        if (not getattr(settings, "ALLOW_USER_OVERRIDE_FOR_WRITE", False) and
                UserService().get_override_user() is not None):
            raise OverrideNotPermitted()

    def get_access_group(self, request, require_manager=False):
        return AccessGroup.objects.access_group_for_user(
            request, require_manager=require_manager)

    def response_ok(self, content):
        return Response(content, status=status.HTTP_200_OK)

    def response_created(self, content):
        return Response(content, status=status.HTTP_201_CREATED)

    def response_badrequest(self, content="Missing parameters"):
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def response_unauthorized(self, content="Not authorized"):
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
