# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.views.api import BaseAPIView, TokenAPIView
from compass.models import Visit, Student, AccessGroup, VisitType
from compass.serializers import VisitReadSerializer, VisitTypeSerializer
from uw_person_client import UWPersonClient
from rest_framework.response import Response
from rest_framework import status
from dateutil import parser
from dateutil.tz import UTC
from logging import getLogger


logger = getLogger(__name__)


class VisitView(BaseAPIView):
    '''
    API endpoint for visit

    /api/internal/visit/(visitid)/
    '''
    def get(self, request, visitid):
        try:
            visit = Visit.objects.get(id=visitid)
        except Visit.DoesNotExist:
            return self.response_notfound()

        serializer = VisitReadSerializer(visit, many=False)
        return self.response_ok(serializer.data)


class VisitOMADView(TokenAPIView):
    '''
    API endpoint for Instructional Center visit recording

    /api/v1/visit/omad/

    {
        "student_netid": "<UW NETID>",
        "visit_type": "<VisitType Name>",
        "course_code": "<Course_Curriculum Course_Number>",
        "checkin_date": "<TIMESTAMP>",
        "checkout_date": "<TIMESTAMP>",
    }
    '''
    def _valid_student(self, netid):
        if netid is None:
            raise ValueError('Missing Student NetID')

        try:
            person = UWPersonClient().get_person_by_uwnetid(
                netid, include_employee=False, include_student=True,
                include_student_transcripts=False,
                include_student_transfers=False, include_student_sports=False,
                include_student_advisers=False, include_student_majors=False,
                include_student_pending_majors=False,
                include_student_holds=False, include_student_degrees=False)
        except Exception as ex:
            raise ValueError(f'IC Visit Error: {netid}: {ex}')

        syskey = person.student.system_key
        student, created = Student.objects.get_or_create(system_key=syskey)
        return student

    def _valid_visit_type(self, name, access_group):
        if name is None:
            raise ValueError('Missing Visit Type')

        try:
            return VisitType.objects.get(access_group=access_group, name=name)
        except VisitType.DoesNotExist:
            raise ValueError(f'Unrecognized visit type: {name}')

    def _valid_course(self, course_code):
        return course_code or "None"

    def _valid_date(self, date_str):
        # parse checkin date
        if date_str is None:
            return None

        try:
            dt = parser.parse(date_str, tzinfos={'PDT': 'UTC-7'})
            if dt.tzinfo is None:
                raise ValueError("Invalid check-in date, missing timezone")
            return dt.astimezone(UTC)
        except parser.ParserError as e:
            raise ValueError(f"Invalid check-in date: {e}")

    def post(self, request, contactid=None):
        try:
            access_group = AccessGroup.objects.by_name("OMAD")
            student = self._valid_student(request.data.get(
                'student_netid'))
            visit_type = self._valid_visit_type(request.data.get(
                'visit_type'), access_group)
            course_code = self._valid_course(request.data.get(
                'course_code'))
            checkin_date = self._valid_date(request.data.get(
                'checkin_date'))
            checkout_date = self._valid_date(request.data.get(
                'checkout_date'))
        except AccessGroup.DoesNotExist as e:
            return Response(repr(e), status=status.HTTP_501_NOT_IMPLEMENTED)
        except ValueError as e:
            return Response(repr(e), status=status.HTTP_400_BAD_REQUEST)

        if checkin_date is None and checkout_date is None:
            return Response("Missing Visit Dates",
                            status=status.HTTP_400_BAD_REQUEST)

        visit, created = Visit.objects.update_or_create(
            student=student, access_group=access_group,
            course_code=course_code, checkin_date=checkin_date,
            defaults={
                'checkout_date': checkout_date,
                'visit_type': visit_type})

        logger.info(f"IC Visit {visit.visit_type} added for "
                    f"student {student.system_key}")
        return Response(status=status.HTTP_201_CREATED)
