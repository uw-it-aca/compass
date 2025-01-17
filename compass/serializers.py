# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.models import (
    Student,
    AppUser,
    AccessGroup,
    Contact,
    ContactTopic,
    ContactType,
    ContactMethod,
    Affiliation,
    Cohort,
    Visit,
    VisitType,
    StudentAffiliation,
    StudentEligibility,
    EligibilityType,
    SpecialProgram,
)
from rest_framework import serializers
import pytz


class AppUserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField()

    class Meta:
        model = AppUser
        fields = ["id", "uwnetid", "display_name"]
        extra_kwargs = {
            "uwnetid": {"validators": []},
        }


class AccessGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessGroup
        fields = ["id", "name", "access_group_id"]
        extra_kwargs = {
            "name": {"validators": []},
            "access_group_id": {"validators": []},
        }


class AffiliationSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = Affiliation
        fields = ["id", "access_group", "name", "slug", "active", "editable"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data["access_group"]["access_group_id"]
        )
        validated_data["access_group"] = access_group
        return Affiliation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance


class CohortReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ["start_year", "end_year"]


class StudentAffiliationReadSerializer(serializers.ModelSerializer):
    affiliation = AffiliationSerializer()
    cohorts = CohortReadSerializer(read_only=True, many=True)

    class Meta:
        model = StudentAffiliation
        fields = [
            "id",
            "student",
            "affiliation",
            "cohorts",
            "date",
            "actively_advised",
        ]


class ContactTopicSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = ContactTopic
        fields = ["id", "access_group", "name", "slug", "active", "editable"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data["access_group"]["access_group_id"]
        )
        validated_data["access_group"] = access_group
        return ContactTopic.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance


class ContactTypeSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = ContactType
        fields = ["id", "access_group", "name", "slug", "active", "editable"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data["access_group"]["access_group_id"]
        )
        validated_data["access_group"] = access_group
        return ContactType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance


class ContactMethodSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = ContactMethod
        fields = ["id", "access_group", "name", "slug", "active", "editable"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data["access_group"]["access_group_id"]
        )
        validated_data["access_group"] = access_group
        return ContactMethod.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.active = validated_data.get("active", instance.active)
        instance.save()
        return instance


class ContactReadSerializer(serializers.ModelSerializer):
    app_user = AppUserSerializer(many=False, read_only=False)
    contact_type = ContactTypeSerializer(many=False, read_only=False)
    contact_method = ContactMethodSerializer(many=False, read_only=False)
    contact_topics = ContactTopicSerializer(many=True, read_only=False)
    created_date = serializers.DateTimeField(default_timezone=pytz.utc)
    checkin_date = serializers.DateTimeField(default_timezone=pytz.utc)
    access_group = AccessGroupSerializer(many=True, read_only=False)
    source = serializers.CharField(
        max_length=None,
        min_length=None,
        allow_blank=False,
        trim_whitespace=True,
    )
    trans_id = serializers.CharField(
        max_length=None,
        min_length=None,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model = Contact
        fields = [
            "id",
            "app_user",
            "student",
            "created_date",
            "checkin_date",
            "notes",
            "actions",
            "contact_type",
            "contact_method",
            "contact_topics",
            "source",
            "trans_id",
            "access_group"
        ]


class ContactWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "app_user",
            "student",
            "created_date",
            "checkin_date",
            "notes",
            "actions",
            "contact_type",
            "contact_method",
            "contact_topics",
            "access_group",
        ]

    def create(self, validated_data):
        contact_topics = validated_data["contact_topics"]
        access_groups = validated_data["access_group"]
        del validated_data["contact_topics"]
        del validated_data["access_group"]
        contact = Contact(**validated_data)
        contact.save()
        contact.contact_topics.set(contact_topics)
        contact.access_group.set(access_groups)
        return contact

    def update(self, instance, validated_data):
        instance.checkin_date = validated_data.get(
            "checkin_date", instance.checkin_date
        )
        instance.notes = validated_data.get("notes", instance.notes)
        instance.actions = validated_data.get("actions", instance.actions)
        instance.contact_type = validated_data.get(
            "contact_type", instance.contact_type
        )
        instance.contact_method = validated_data.get(
            "contact_method", instance.contact_method
        )
        instance.contact_topics.set(
            validated_data.get("contact_topics", instance.contact_topics)
        )
        instance.save()
        return instance


class StudentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "system_key", "programs"]

    def create(self, validated_data):
        student_programs = validated_data["programs"]
        del validated_data["programs"]
        student = Student(**validated_data)
        student.save()
        student.programs.set(student_programs)
        return student

    def update(self, instance, validated_data):
        instance.system_key = validated_data.get(
            "system_key", instance.system_key
        )
        instance.programs.set(
            validated_data.get("programs", instance.programs)
        )
        instance.save()
        return instance


class VisitTypeSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = VisitType
        fields = ["id", "access_group", "name", "slug", "editable"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data["access_group"]["access_group_id"]
        )
        validated_data["access_group"] = access_group
        return VisitType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class VisitReadSerializer(serializers.ModelSerializer):
    visit_type = VisitTypeSerializer(many=False, read_only=False)
    checkin_date = serializers.DateTimeField(default_timezone=pytz.utc)
    checkout_date = serializers.DateTimeField(default_timezone=pytz.utc)

    class Meta:
        model = Visit
        fields = [
            "id",
            "student",
            "visit_type",
            "course_code",
            "checkin_date",
            "checkout_date",
        ]


class EligibilityTypeSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)

    class Meta:
        model = EligibilityType
        fields = ["id", "access_group", "name", "slug", "editable"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }

    def create(self, validated_data):
        access_group = AccessGroup.objects.get(
            access_group_id=validated_data["access_group"]["access_group_id"]
        )
        validated_data["access_group"] = access_group
        return EligibilityType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class StudentEligibilitySerializer(serializers.ModelSerializer):
    eligibility = EligibilityTypeSerializer(read_only=True, many=True)

    class Meta:
        model = StudentEligibility
        fields = ["id", "student", "eligibility"]


class SpecialProgramSerializer(serializers.ModelSerializer):
    access_group = AccessGroupSerializer(many=False, read_only=False)
    modified_by = AppUserSerializer(many=False, read_only=False)

    class Meta:
        model = SpecialProgram
        fields = [
            "id",
            "access_group",
            "program_date",
            "modified_by",
            "modified_date"]
        extra_kwargs = {
            "access_group_id": {"validators": []},
        }
