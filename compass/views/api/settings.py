# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import ContactTopic, ContactType, Program
from compass.serializers import ProgramSerializer, ContactTopicSerializer, \
    ContactTypeSerializer
from compass.views.api import BaseAPIView
from rest_framework.response import Response
from rest_framework import status

class SettingsView(BaseAPIView):
    '''
    API endpoint returning a list of programs for the user's access group

    /api/internal/settings/
    '''

    def get(self, request):
        access_groups = self.get_access_groups(request)

        settings_by_group = {}
        for access_group in access_groups:
            group_settings = {}
            # programs
            program_serializer = ProgramSerializer(
                Program.objects.filter(access_group=access_group.id),
                many=True)
            group_settings["programs"] = program_serializer.data
            # contact topics
            contact_topic_serializer = ContactTopicSerializer(
                ContactTopic.objects.filter(access_group=access_group.id),
                many=True)
            group_settings["contact_topics"] = contact_topic_serializer.data
            # contact types
            contact_type_serializer = ContactTypeSerializer(
                ContactType.objects.filter(access_group=access_group.id),
                many=True)
            group_settings["contact_types"] = contact_type_serializer.data
            settings_by_group[access_group.name] = group_settings
        return Response(settings_by_group, status=status.HTTP_200_OK)