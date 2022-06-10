# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import Contact, ContactTopic, ContactType
from rest_framework import serializers


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'author', 'student', 'pub_date', 'date', 'time',
                  'notes', 'actions', 'contact_type', 'contact_topics']

    def create(self, validated_data):
        contact_topics = validated_data['contact_topics']
        del validated_data['contact_topics']
        contact = Contact(**validated_data)
        contact.save()
        contact.contact_topics.set(contact_topics)
        return contact

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.time = validated_data.get('time', instance.time)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.actions = validated_data.get('actions', instance.actions)
        instance.contact_type = \
            validated_data.get('contact_type', instance.contact_type)
        instance.contact_topics.set(
            validated_data.get('contact_topics', instance.contact_topics))
        return instance


class ContactTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactTopic
        fields = ['id', 'name']


class ContactTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactType
        fields = ['id', 'name']
