# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import ContactTopic, ContactType, ContactMethod, Program
from compass.serializers import ProgramSerializer, ContactTopicSerializer, \
    ContactTypeSerializer, ContactMethodSerializer
from compass.views.api import BaseAPIView
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


class SettingsView(BaseAPIView):
    '''
    API endpoint returning a list of programs for the user's access group

    /api/internal/accessgroup/[access_group_pk]/settings/[setting_type]/

    The setting_type param can be: program, contact_topic, or contact_type
    '''

    def get(self, request, access_group_pk, setting_type):
        try:
            access_group = self.validate_manager_access(
                request, access_group_pk)

            group_settings = []
            if setting_type == "program":
                # programs
                program_serializer = ProgramSerializer(
                    Program.objects.filter(access_group=access_group.id),
                    many=True)
                group_settings = program_serializer.data
            elif setting_type == "contact_topic":
                # contact topics
                contact_topic_serializer = ContactTopicSerializer(
                    ContactTopic.objects.filter(access_group=access_group.id),
                    many=True)
                group_settings = contact_topic_serializer.data
            elif setting_type == "contact_type":
                # contact types
                contact_type_serializer = ContactTypeSerializer(
                    ContactType.objects.filter(access_group=access_group.id),
                    many=True)
                group_settings = contact_type_serializer.data
            elif setting_type == "contact_method":
                # contact methods
                contact_type_serializer = ContactMethodSerializer(
                    ContactMethod.objects.filter(access_group=access_group.id),
                    many=True)
                group_settings = contact_type_serializer.data
            else:
                return Response(f"Unknown setting type '{setting_type}'",
                                status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response(f"User not authorized to access '{setting_type}' "
                            f"settings for access group '{access_group_pk}'",
                            status=status.HTTP_401_UNAUTHORIZED)
        # return settings
        return Response(group_settings, status=status.HTTP_200_OK)

    def post(self, request, access_group_pk, setting_type):
        """
        API endpoint for saving a list of settings

        /api/internal/accessgroup/[access_group_pk]/settings/[setting_type]/
        """
        try:
            self.validate_manager_access(
                request, access_group_pk)
            # get setting values to create or update
            setting_values = request.data["setting_values"]
            # associate the correct model and serializer with the setting type
            SETTING_MODEL_CLS = None
            SETTING_SERIALIZER_CLS = None
            if setting_type == "program":
                SETTING_MODEL_CLS = Program
                SETTING_SERIALIZER_CLS = ProgramSerializer
            elif setting_type == "contact_topic":
                SETTING_MODEL_CLS = ContactTopic
                SETTING_SERIALIZER_CLS = ContactTopicSerializer
            elif setting_type == "contact_type":
                SETTING_MODEL_CLS = ContactType
                SETTING_SERIALIZER_CLS = ContactTypeSerializer
            elif setting_type == "contact_Method":
                SETTING_MODEL_CLS = ContactMethod
                SETTING_SERIALIZER_CLS = ContactMethodSerializer

            # save each setting
            setting_saves = []
            for setting_val in setting_values:
                try:
                    # update existing setting record if one exists
                    setting = \
                        SETTING_MODEL_CLS.objects.get(id=setting_val['id'])
                    serializer = SETTING_SERIALIZER_CLS(setting,
                                                        data=setting_val)
                except SETTING_MODEL_CLS.DoesNotExist:
                    # create new setting
                    serializer = SETTING_SERIALIZER_CLS(data=setting_val)
                if serializer.is_valid():
                    serializer.save()
                    setting_saves.append(serializer.data)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
                # return settings
                return Response(setting_saves, status=status.HTTP_200_OK)
        except PermissionDenied:
            return Response(f"User not authorized to access '{setting_type}' "
                            f"settings for access group '{access_group_pk}'",
                            status=status.HTTP_401_UNAUTHORIZED)
