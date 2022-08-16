# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import AppUser, AccessGroup, Contact, ContactTopic, \
    ContactType, Program, Student
from rest_framework import serializers


class AppUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUser
        fields = ['id', 'uwnetid']
        extra_kwargs = {
            'uwnetid': {'validators': []},
        }


class AccessGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessGroup
        fields = ['id', 'name', 'access_group_id']
        extra_kwargs = {
            'name':  {'validators': []},
            'access_group_id': {'validators': []},
        }


class ProgramSerializer(serializers.ModelSerializer):

    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = Program
        fields = ['id', 'access_group', 'name', 'active']
        extra_kwargs = {
            'access_group_id': {'validators': []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data['access_group']['access_group_id'])
        validated_data["access_group"] = access_group
        return Program.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


class ContactTopicSerializer(serializers.ModelSerializer):

    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = ContactTopic
        fields = ['id', 'access_group', 'name', 'active']
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        return ContactTopic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class ContactTypeSerializer(serializers.ModelSerializer):

    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = ContactType
        fields = ['id', 'access_group', 'name', 'active']
        extra_kwargs = {
            'name': {'validators': []},
        }

    def create(self, validated_data):
        return ContactType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


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
        instance.save()
        return instance


class StudentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'system_key', 'programs']

    def create(self, validated_data):
        student_programs = validated_data['programs']
        del validated_data['programs']
        student = Student(**validated_data)
        student.save()
        student.programs.set(student_programs)
        return student

    def update(self, instance, validated_data):
        instance.system_key = validated_data.get(
            'system_key', instance.system_key)
        instance.programs.set(
            validated_data.get('programs', instance.programs))
        instance.save()
        return instance
