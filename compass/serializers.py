# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import AppUser, Contact, ContactTopic, ContactType
from rest_framework import serializers


class ContactTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactTopic
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        print("CREATE CONTACT TOPICS")
        return ContactTopic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("UPDATE CONTACT TOPICS")
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ContactTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactType
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        print("CREATE CONTACT TYPE")
        return ContactType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("UPDATE CONTACT TYPE")
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ['id', 'uwnetid']
        extra_kwargs = {
            'uwnetid': {'validators': []},
        }


class ContactReadSerializer(serializers.ModelSerializer):

    author = AppUserSerializer(many=False, read_only=False)
    contact_type = ContactTypeSerializer(many=False, read_only=False)
    contact_topics = ContactTopicSerializer(many=True, read_only=False)

    class Meta:
        model = Contact
        fields = ['id', 'author', 'student', 'pub_date', 'date', 'time',
                  'notes', 'actions', 'contact_type', 'contact_topics']

class ContactWriteSerializer(serializers.ModelSerializer):

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
