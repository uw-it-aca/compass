# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import Retention, Student, Major, Retention, SpecialProgram
from rest_framework import serializers


class RetentionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Retention
        fields = ['priority',
                  'sign_in',
                  'activity',
                  'assignment',
                  'grade']


class SpecialProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialProgram
        fields = ['special_program_code',
                  'special_program_desc']


class MajorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Major
        fields = ['major_abbr_code',
                  'major_full_code',
                  'major_name',
                  'major_full_name',
                  'major_short_name']


class StudentSerializer(serializers.ModelSerializer):
    intended_major = MajorSerializer(many=True, read_only=True)
    major = MajorSerializer(many=True, read_only=True)
    retention = RetentionSerializer(read_only=True)
    special_program = SpecialProgramSerializer(many=True, read_only=True)
    adviser_full_name = \
        serializers.CharField(source="adviser.full_name", read_only=True)
    enrollment_desc = serializers.ReadOnlyField()

    class Meta:
        model = Student
        fields = ['id',
                  'student_number',
                  'uw_net_id',
                  'student_name',
                  'student_preferred_first_name',
                  'student_preferred_middle_name',
                  'student_preferred_last_name',
                  'birthdate',
                  'student_email',
                  'external_email',
                  'local_phone_number',
                  'gender',
                  'gpa',
                  'total_credits',
                  'total_uw_credits',
                  'campus_desc',
                  'class_desc',
                  'enrollment_status_code',
                  'enrollment_desc',
                  'retention',
                  'special_program',
                  'honors_program_code',
                  'resident_desc',
                  'perm_addr_line1',
                  'perm_addr_line2',
                  'perm_addr_city',
                  'perm_addr_state',
                  'perm_addr_5digit_zip',
                  'perm_addr_4digit_zip',
                  'perm_addr_country',
                  'perm_addr_postal_code',
                  'registered_in_quarter',
                  'intended_major',
                  'major',
                  'adviser_full_name']
