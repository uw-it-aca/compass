# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import Contact, ContactTopic
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['author', 'pub_date', 'time', 'notes', 'actions',
                  'contact_type', 'contact_topics']
