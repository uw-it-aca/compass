# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.models import Student
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    major_full_name = \
        serializers.CharField(source="major.major_full_name", read_only=True)
    adviser_full_name = \
        serializers.CharField(source="adviser.full_name", read_only=True)

    class Meta:
        model = Student
        fields = ['student_name',
                  'student_number',
                  'uw_net_id',
                  'class_desc',
                  'enrollment_status',
                  'gender',
                  'major_full_name',
                  'adviser_full_name']
