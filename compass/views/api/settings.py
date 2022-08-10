# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import ContactTopic, ContactType, Program, AccessGroup
from compass.serializers import ProgramSerializer, ContactTopicSerializer, \
    ContactTypeSerializer
from compass.views.api import BaseAPIView
from rest_framework.response import Response
from rest_framework import status

class SettingsView(BaseAPIView):
    '''
    API endpoint returning a list of programs for the user's access group

    /api/internal/settings/[access_group]/[setting_type]/

    The setting_type param can be: program, contact_topic, or contact_type
    '''

    def get(self, request, setting_type, access_group_id):
        # check if user can access requested access_group settings
        access_group_memberships = self.get_access_groups(request)
        access_group_ids = [access_group.access_group_id
                            for access_group in access_group_memberships]
        if access_group_id not in access_group_ids:
            return Response(f"User not authorized to access settings for "
                            f"access group '{access_group_id}'",
                            status=status.HTTP_401_UNAUTHORIZED) 
        access_group = AccessGroup.objects.get(access_group_id=access_group_id)
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
        else:
            return Response(f"Unknown setting type '{setting_type}'",
                            status=status.HTTP_400_BAD_REQUEST)

        # return settings
        return Response(group_settings, status=status.HTTP_200_OK)


#    def post(self, request):
#        pass