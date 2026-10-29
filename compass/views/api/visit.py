# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import date
from logging import getLogger
from tempfile import SpooledTemporaryFile

from dateutil import parser
from dateutil.tz import UTC
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response

from compass.dao.compass_visits import (
    DataFailureException,
    admin_create_visit,
    admin_delete_visit,
    admin_update_visit,
    get_admin_visit_list,
    get_visit_options,
)
from compass.dao.person import (
    PersonNotFoundException,
    get_appuser_by_uwnetid,
    get_person_by_student_number,
    get_person_by_uwnetid,
    valid_student_number,
    valid_system_key,
    valid_uwnetid,
)
from compass.dao.term import current_term
from compass.dao.visit_file import (
    create_visits_from_file,
    get_visit_export,
    validate_visit_upload_file,
)
from compass.models import (
    AccessGroup,
    Student,
    Visit,
    VisitTutoringOption,
    VisitType,
)
from compass.serializers import ExternalVisitSerializer, VisitReadSerializer
from compass.views.api import BaseAPIView, TokenAPIView

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
    """
    API endpoint for Instructional Center visit recording

    /api/v1/visit/omad/

    {
        "student_netid": "<UW NETID>",
        "visit_type": "<VisitType Name>",
        "course_code": "<Course_Curriculum Course_Number>",
        "tutoring_option": "<TutoringOption Name>",
        "checkin_date": "<TIMESTAMP>",
        "checkout_date": "<TIMESTAMP>",
    }
    """

    def _valid_student(self, netid):
        if netid is None:
            raise ValueError('Missing Student NetID')

        try:
            person = get_appuser_by_uwnetid(netid)
        except Exception as ex:
            raise ValueError(f'IC Visit Error: {netid}: {ex}')

        student, _ = Student.objects.get_or_create(
            system_key=person.system_key)
        return student

    def _valid_visit_type(self, value, access_group):
        if value is None:
            raise ValueError('Missing Visit Type')

        try:
            return VisitType.objects.get(
                access_group=access_group,
                slug=value,
                is_compass_visits_program_area=True)
        except VisitType.DoesNotExist:
            try:
                return VisitType.objects.get(
                    access_group=access_group,
                    name=value,
                    is_compass_visits_program_area=True)
            except VisitType.DoesNotExist:
                raise ValueError(f'Unrecognized visit type: {value}')

    def _valid_course(self, course_code):
        return course_code or "None"

    def _valid_tutoring_option(self, value, access_group):
        # Don't require a tutoring option until we switch off the Legacy IC
        if value is None:
            return None

        try:
            return VisitTutoringOption.objects.get(
                access_group=access_group, slug=value)
        except VisitTutoringOption.DoesNotExist:
            try:
                return VisitTutoringOption.objects.get(
                    access_group=access_group, name=value)
            except VisitTutoringOption.DoesNotExist:
                raise ValueError(f'Unrecognized tutoring option: {value}')

    def _valid_date(self, date_str):
        # parse checkin date
        if date_str is None:
            return None

        try:
            dt = parser.parse(date_str,
                              tzinfos=getattr(settings, "TZINFOS", {}))
            if dt.tzinfo is None:
                raise ValueError("Invalid check-in date, missing timezone")
            return dt.astimezone(UTC)
        except parser.ParserError as e:
            raise ValueError(f"Invalid check-in date: {e}")

    def post(self, request, contactid=None):
        try:
            access_group = AccessGroup.objects.by_name(
                settings.COMPASS_VISITS_ACCESS_GROUP_NAME)
            student = self._valid_student(request.data.get(
                'student_netid'))
            visit_type = self._valid_visit_type(request.data.get(
                'visit_type'), access_group)
            course_code = self._valid_course(request.data.get(
                'course_code'))
            tutoring_option = self._valid_tutoring_option(request.data.get(
                'tutoring_option'), access_group)
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

        visit, _ = Visit.objects.update_or_create(
            student=student, access_group=access_group,
            course_code=course_code, checkin_date=checkin_date,
            defaults={
                'checkout_date': checkout_date,
                'visit_type': visit_type,
                'tutoring_option': tutoring_option})

        logger.info(f"IC Visit {visit.visit_type} added for "
                    f"student {student.system_key}")
        return Response(status=status.HTTP_201_CREATED)


class VisitCatalogView(TokenAPIView):
    """Return the Compass-owned OMAD visit catalog."""

    def get(self, request):
        try:
            access_group = AccessGroup.objects.by_name(
                settings.COMPASS_VISITS_ACCESS_GROUP_NAME)
        except AccessGroup.DoesNotExist as e:
            return Response(repr(e),
                            status=status.HTTP_501_NOT_IMPLEMENTED)

        return Response({
            "visit_types": list(
                VisitType.objects.filter(
                    access_group=access_group,
                    is_compass_visits_program_area=True)
                .order_by("id")
                .values("id", "name", "slug")
            ),
            "tutoring_options": list(
                VisitTutoringOption.objects.filter(access_group=access_group)
                .order_by("id")
                .values("id", "name", "slug")
            ),
        })


class ActiveICVisitListView(BaseAPIView):
    '''
    API endpoint for active IC visits
    (pending verification or not checked out)

    /api/internal/ic/active_visits/
    '''

    def get(self, request):
        visits = get_admin_visit_list()
        return self.response_ok(visits)


class VisitSearchMixin:
    def _response_ok(self, content):
        if hasattr(self, 'response_ok'):
            return self.response_ok(content)
        return Response(content, status=status.HTTP_200_OK)

    def _response_badrequest(self, content='Missing parameters'):
        if hasattr(self, 'response_badrequest'):
            return self.response_badrequest(content)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def _response_notfound(self, content='Not found'):
        if hasattr(self, 'response_notfound'):
            return self.response_notfound(content)
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    def _lookup_visits(self, identifier, allow_system_key=False):
        """
        Resolves an identifier to a student and returns the current-quarter
        visits queryset. Returns (visits, None) on success or (None, error_response)
        if the identifier is invalid or the student does not exist.
        """
        student_identifier = identifier.strip().lower()
        try:
            if allow_system_key and valid_system_key(student_identifier):
                system_key = student_identifier
            elif valid_uwnetid(student_identifier):
                system_key = get_person_by_uwnetid(
                    student_identifier).system_key
            elif valid_student_number(student_identifier):
                system_key = get_person_by_student_number(
                    student_identifier).system_key
            else:
                return None, self._response_badrequest(
                    'Invalid student identifier')
        except PersonNotFoundException:
            return None, self._response_notfound('Student not found')

        try:
            student = Student.objects.get(system_key=system_key)
        except Student.DoesNotExist:
            return None, self._response_notfound('Student not found')

        current_qtr_start = current_term().first_day_quarter
        visits = Visit.objects.filter(
            student=student,
            checkin_date__gte=current_qtr_start).order_by('-checkin_date')
        return visits, None

    def _visit_search_response(self, identifier):
        visits, error = self._lookup_visits(identifier)
        if error is not None:
            return error
        serializer = VisitReadSerializer(visits, many=True)
        return self._response_ok(serializer.data)


class VisitSearchView(VisitSearchMixin, BaseAPIView):
    '''
    API endpoint for searching visits by student number or netid
    /api/internal/visits/search/[identifier]/
     where identifier is either a student number or a netid
     (e.g. 12345678 or jsmith)
    '''

    def get(self, request, identifier):
        return self._visit_search_response(identifier)


class ICVisitOptionsView(BaseAPIView):
    '''
    API endpoint for retrieving IC visit options
    /api/internal/visit_options/[uwregid]/
    where [uwregid] is the UW regid of the student
    '''

    def get(self, request, uwregid):
        visit_options = get_visit_options(uwregid)
        return self.response_ok(visit_options)


class ICVisitCreateView(BaseAPIView):
    '''
    API endpoint for creating or updating IC visits
    /api/internal/create_visit
    '''

    def post(self, request):
        visit_data = request.data
        try:
            visit = admin_create_visit(visit_data)
            return self.response_ok(visit.json_data())
        except DataFailureException as e:
            logger.error(f"Error creating IC visit: {e}")
            return self.response_badrequest(f"Error creating IC visit: {e}")


class ICVisitUpdateView(BaseAPIView):
    '''
    API endpoint for updating IC visits
    /api/internal/update_visit/[visit_id]
    '''

    def patch(self, request, visit_id):
        is_verified = request.data.get('is_verified', False)
        is_checked_out = request.data.get('is_checked_out', False)
        try:
            visit = admin_update_visit(visit_id, is_verified, is_checked_out)
            return self.response_ok(visit.json_data())
        except DataFailureException as e:
            logger.error(f"IC visit not found: {e}")
            return self.response_notfound(f"IC visit not found: {e}")
        except Exception as e:
            logger.error(f"Error updating IC visit: {e}")
            return self.response_badrequest(f"Error updating IC visit: {e}")

    def delete(self, request, visit_id):
        try:
            admin_delete_visit(visit_id)
            return self.response_deleted()
        except DataFailureException as e:
            logger.error(f"IC visit not found: {e}")
            return self.response_notfound(f"IC visit not found: {e}")
        except Exception as e:
            logger.error(f"Error deleting IC visit: {e}")
            return self.response_badrequest(f"Error deleting IC visit: {e}")


class ICVisitFileView(BaseAPIView):
    '''
    API endpoint for handling IC visit uploads and exports
    /api/internal/visit/file/
    POST: upload visit data from file
    GET: export visits by inclusive check-in start_date and end_date
    (YYYY-MM-DD in the application timezone; at most 366 days/50,000 visits)
    '''

    MAX_EXPORT_DAYS = 366
    MAX_EXPORT_VISITS = 50000
    EARLIEST_EXPORT_DATE = date(2008, 1, 1)

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return self.response_badrequest('No file uploaded')
        is_valid, error_message = validate_visit_upload_file(file)
        if not is_valid:
            return self.response_badrequest(error_message)
        file.seek(0)
        visit_type = request.data.get('visit_type')
        tutoring_option = request.data.get('tutoring_option')
        date = request.data.get('date')
        if not visit_type or not tutoring_option or not date:
            return self.response_badrequest(
                'Missing visit_type, tutoring_option, or date')
        try:
            count_created = create_visits_from_file(file,
                                                    visit_type,
                                                    tutoring_option,
                                                    date)
        except ValueError as e:
            return self.response_badrequest(str(e))

        return self.response_ok({'count_created': count_created})

    def get(self, request):
        try:
            start_date = date.fromisoformat(
                request.query_params.get('start_date', ''))
            end_date = date.fromisoformat(
                request.query_params.get('end_date', ''))
        except (TypeError, ValueError):
            return self.response_badrequest(
                'start_date and end_date are required in YYYY-MM-DD format')
        if end_date < start_date or end_date == date.max:
            return self.response_badrequest('Invalid export date range')
        if start_date < self.EARLIEST_EXPORT_DATE:
            return self.response_badrequest(
                'Visit exports are available from January 1, 2008')
        if (end_date - start_date).days >= self.MAX_EXPORT_DAYS:
            return self.response_badrequest(
                'Export date range cannot exceed 366 days')

        export_file = SpooledTemporaryFile(  # noqa: SIM115 (FileResponse closes it)
            max_size=5 * 1024 * 1024)
        try:
            for row_index, line in enumerate(
                    get_visit_export(start_date, end_date)):
                if row_index > self.MAX_EXPORT_VISITS:
                    export_file.close()
                    return self.response_badrequest(
                        'Export exceeds 50,000 visits; select a smaller '
                        'date range')
                export_file.write(line.encode('utf-8'))
            export_file.seek(0)
        except Exception:
            export_file.close()
            logger.exception('Error preparing IC visit export')
            return Response(
                'Unable to prepare visit export. Try a smaller date range.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = FileResponse(export_file, as_attachment=True,
                                filename='visit_export.csv',
                                content_type='text/csv')
        response['Cache-Control'] = 'no-store'
        return response


class ExternalStudentVisitView(VisitSearchMixin, TokenAPIView):
    '''
    API endpoint for retrieving visits by student system key, student number,
    or netid, to be used by Compass Visits
    '''

    def get(self, request, identifier):
        if settings.COMPASS_VISITS_TOKEN_USER != request.user.username:
            return Response("Unauthorized",
                            status=status.HTTP_401_UNAUTHORIZED)
        visits, error = self._lookup_visits(identifier, allow_system_key=True)
        if error is not None:
            return error
        serializer = ExternalVisitSerializer(visits, many=True)
        return Response(serializer.data)
