# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import reverse
from userservice.user import UserService
from compass.views.api import BaseAPIView
from compass.dao.photo import PhotoDAO
from compass.dao.person import (
    valid_uwnetid, valid_uwregid, valid_student_number, valid_system_key,
    get_person_by_uwnetid, get_person_by_student_number,
    get_transcripts_by_uwregid, PersonNotFoundException)
from compass.dao.csv import StudentCSV
from compass.dao import current_datetime_utc
from compass.models import (
    AccessGroup, Student, AppUser, Contact, ContactType, ContactMethod,
    ContactTopic, StudentAffiliation, Affiliation, Cohort, Visit,
    EligibilityType, StudentEligibility, SpecialProgram)
from compass.models.rad_data import (CourseAnalyticsScores,
                                     StudentSigninAnalytics)
from compass.serializers import (
    ContactReadSerializer, ContactWriteSerializer, StudentWriteSerializer,
    StudentAffiliationReadSerializer, VisitReadSerializer,
    StudentEligibilitySerializer, EligibilityTypeSerializer,
    SpecialProgramSerializer)
from compass.exceptions import OverrideNotPermitted, InvalidCSV
from restclients_core.exceptions import DataFailureException
from uw_sws.term import (
    get_current_term, get_next_term, get_term_after,
    get_term_by_year_and_quarter)
from uw_sws.registration import get_schedule_by_regid_and_term
from logging import getLogger

logger = getLogger(__name__)

TERMS = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Autumn"}


class StudentView(BaseAPIView):
    '''
    API endpoint returning a student's details

    /api/internal/student/[student_number|uwnetid]/
    '''
    def get(self, request, identifier):
        try:
            includes = {
                'include_student': True,
                'include_student_holds': True,
                'include_student_transfers': True,
                'include_student_degrees': True,
            }
            if valid_uwnetid(identifier):
                person = get_person_by_uwnetid(identifier, **includes)
            elif valid_student_number(identifier):
                person = get_person_by_student_number(identifier, **includes)
            else:
                return self.response_badrequest('Invalid student identifier')

            person_dict = person.to_dict()
            photo_key = PhotoDAO().generate_photo_key()
            person_dict['photo_url'] = reverse('photo', kwargs={
                'uwregid': person.uwregid,
                'photo_key': photo_key})
            return self.response_ok(person_dict)
        except PersonNotFoundException:
            return self.response_notfound()

    def post(self, request, identifier=None):
        try:
            access_group = self.get_access_group(request)

            self.valid_user_override()

            data = request.data
            system_key = data.get("system_key")
            if not valid_system_key(system_key):
                return Response('Invalid systemkey',
                                status=status.HTTP_400_BAD_REQUEST)

            student_record = {}
            student_record['system_key'] = system_key
            student_record['programs'] = data.get('programs')
            try:
                # update existing student record if one exists
                student, _ = Student.objects.get_or_create(
                    system_key=system_key)
                serializer = StudentWriteSerializer(student,
                                                    data=student_record)
            except Student.DoesNotExist:
                # create new student record
                serializer = StudentWriteSerializer(data=student_record)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Student {system_key} saved: {serializer.data}")
                return self.response_created(serializer.data)
            else:
                return self.response_badrequest(serializer.errors)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)


class StudentSchedulesView(BaseAPIView):
    '''
    API endpoint returning a student's class schedule details

    /api/internal/student/[uwregid]/schedules/
    '''
    def get(self, request, uwregid):
        if not valid_uwregid(uwregid):
            return self.response_badrequest('Invalid uwregid')

        cur_term = get_current_term()
        next_term = get_next_term()
        term_after = get_term_after(next_term)
        terms = [cur_term, next_term, term_after]
        schedules = {}
        for index, term in enumerate(terms):
            try:
                schedules[index] = get_schedule_by_regid_and_term(
                    uwregid, term).json_data()
            except DataFailureException:
                continue
        updated_schedule = CourseAnalyticsScores.add_alert_status_to_schedules(schedules,
                                                                               uwregid)
        return self.response_ok(updated_schedule)


class StudentContactsView(BaseAPIView):
    '''
    API endpoint returning a list of contacts for a student

    /api/internal/student/[systemkey]/contacts/
    '''
    def get(self, request, systemkey):
        if not valid_system_key(systemkey):
            return self.response_badrequest('Invalid systemkey')

        queryset = Contact.objects.filter(
            student__system_key__contains=systemkey.lstrip("0"))\
            .order_by('-checkin_date')
        serializer = ContactReadSerializer(queryset, many=True)
        return self.response_ok(serializer.data)


class StudentAffiliationsView(BaseAPIView):
    '''
    API endpoint returning a list of affiliations for a student

    /api/internal/student/[systemkey]/affiliations/
    '''

    def get(self, request, systemkey):
        affiliations = []
        try:
            access_group = self.get_access_group(request)

            if not valid_system_key(systemkey):
                return self.response_badrequest('Invalid systemkey')

            student_affiliations = StudentAffiliation.objects.filter(
                student__system_key=systemkey,
                affiliation__access_group=access_group)

            for sa in student_affiliations:
                affiliations.append(
                    StudentAffiliationReadSerializer(sa).data)
        except StudentAffiliation.DoesNotExist:
            pass
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        return self.response_ok(affiliations)

    def post(self, request, systemkey, affiliation_id=None):
        try:
            access_group = self.get_access_group(request)

            self.valid_user_override()

            if not valid_system_key(systemkey):
                return self.response_badrequest('Invalid systemkey')

            affiliation_data = request.data.get('affiliation')

            student = Student.objects.get(system_key=systemkey)

            affiliation_model_id = int(affiliation_data['affiliationId'])
            affiliation = Affiliation.objects.get(
                id=affiliation_model_id, access_group=access_group)

            if affiliation_id:
                sa = StudentAffiliation.objects.get(id=affiliation_id)
                sa.affiliation = affiliation
            else:
                sa, _ = StudentAffiliation.objects.get_or_create(
                    student=student, affiliation=affiliation)

            sa.actively_advised = affiliation_data['actively_advised']
            sa.date = current_datetime_utc().date()

            cohort_objects = []
            for c in affiliation_data['cohorts']:
                co, _ = Cohort.objects.get_or_create(
                    start_year=c['start_year'], end_year=c['end_year'])
                cohort_objects.append(co)

            sa.cohorts.clear()
            for cohort in cohort_objects:
                sa.cohorts.add(cohort)

            sa.save()

            serializer = StudentAffiliationReadSerializer(sa)
            logger.info(f"StudentAffiliation for {systemkey} saved: "
                        f"{serializer.data}")
            return self.response_ok(serializer.data)
        except Student.DoesNotExist:
            return self.response_notfound("Unknown student")
        except StudentAffiliation.DoesNotExist:
            return self.response_notfound("Unknown student affiliation")
        except Affiliation.DoesNotExist:
            return self.response_notfound("Unknown or unpermitted affiliation")
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

    def delete(self, request, systemkey, affiliation_id):
        try:
            access_group = self.get_access_group(request)

            self.valid_user_override()

            if not valid_system_key(systemkey):
                return self.response_badrequest('Invalid systemkey')

            student = Student.objects.get(system_key=systemkey)

            student_affiliation = StudentAffiliation.objects.get(
                id=affiliation_id, student=student,
                affiliation__access_group=access_group)
            student_affiliation.delete()
            logger.info(f"StudentAffiliation {affiliation_id} for "
                        f"{systemkey} deleted")
            return self.response_ok("")
        except Student.DoesNotExist:
            return self.response_notfound("Unknown student")
        except StudentAffiliation.DoesNotExist:
            return self.response_notfound("Unknown student affiliation")
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)


class StudentAffiliationsImportView(BaseAPIView):
    '''
    API endpoint for assigning the passed affiliation to multiple students

    /api/internal/import/affiliations/[affiliation_id]
    '''
    def post(self, request, *args, **kwargs):
        try:
            access_group = self.get_access_group(request, require_manager=True)
            self.valid_user_override()
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)

        affiliation_id = kwargs.get("affiliation_id")
        try:
            affiliation = Affiliation.objects.get(
                id=affiliation_id, access_group=access_group)
        except Affiliation.DoesNotExist:
            return self.response_badrequest(
                content="Unknown or unpermitted affiliation")

        cohort_str = request.data.get("cohort")
        try:
            (start, end) = cohort_str.split("-", maxsplit=1)
            cohort = Cohort.objects.get(start_year=start, end_year=end)
        except AttributeError:
            return self.response_badrequest("Missing cohort")
        except (ValueError, Cohort.DoesNotExist):
            return self.response_badrequest(f"Unknown cohort {cohort_str}")

        uploaded_file = request.FILES.get("file")
        if uploaded_file is None:
            return self.response_badrequest(content="Missing file")

        try:
            person_data = StudentCSV().students_from_file(uploaded_file)
        except InvalidCSV as ex:
            logger.info(
                f"POST upload failed for {uploaded_file.name}: {ex.error}")
            return self.response_badrequest(f"Invalid CSV file: {ex.error}")

        contact_dict = {
            'app_user': AppUser.objects.upsert_appuser(
                UserService().get_user()).id,
            'student': None,
            'access_group': [access_group.id],
            'contact_type': ContactType.objects.get(slug='admin').id,
            'contact_method': ContactMethod.objects.get(slug='internal').id,
            'contact_topics': [ContactTopic.objects.get(slug='other').id],
            'checkin_date': current_datetime_utc(),
            'notes': 'Affiliation updated by batch import',
        }

        for p in person_data:
            if "error" in p:
                continue

            student, _ = Student.objects.get_or_create(
                system_key=p["system_key"])

            sa, _ = StudentAffiliation.objects.get_or_create(
                student=student, affiliation=affiliation)

            sa.date = current_datetime_utc().date()
            sa.cohorts.add(cohort)
            sa.save()

            # Create a Contact from advisor type 'Admin'
            contact_dict['student'] = student.id
            contact_serializer = ContactWriteSerializer(data=contact_dict)
            if contact_serializer.is_valid():
                contact_serializer.save()

            logger.info(
                f"StudentAffiliation for {student.system_key} added: "
                f"{affiliation.name} ({affiliation.id}), {cohort_str}")

            sa_serializer = StudentAffiliationReadSerializer(sa)
            p['affiliation'] = sa_serializer.data

        return self.response_ok(person_data)


class StudentVisitsView(BaseAPIView):
    '''
    API endpoint returning a list of visits for a student

    /api/internal/student/[systemkey]/visits/
    '''
    def get(self, request, systemkey):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        if not valid_system_key(systemkey):
            return self.response_badrequest('Invalid systemkey')

        queryset = Visit.objects.filter(
            student__system_key=systemkey,
            visit_type__access_group=access_group).order_by('-checkin_date')
        serializer = VisitReadSerializer(queryset, many=True)
        return self.response_ok(serializer.data)


class StudentTranscriptsView(BaseAPIView):
    '''
    API endpoint returning a list of transcripts for a student

    /api/internal/student/[uwregid]/transcripts/
    '''
    def get(self, request, uwregid):
        try:
            transcripts = get_transcripts_by_uwregid(uwregid)
        except PersonNotFoundException as ex:
            return self.response_notfound("Unknown student")

        transcript_data = []
        for transcript in transcripts:
            transcript_dict = transcript.to_dict()
            try:
                term = get_term_by_year_and_quarter(
                    transcript.tran_term.year,
                    TERMS[transcript.tran_term.quarter])

                class_schedule = get_schedule_by_regid_and_term(
                    uwregid, term)
                transcript_dict['class_schedule'] = class_schedule.json_data()
            except DataFailureException as ex:
                logger.info(
                    f'Error fetching class schedule for {uwregid}: {ex}')
                transcript_dict['class_schedule'] = None
            transcript_data.append(transcript_dict)

        return self.response_ok(transcript_data)


class StudentEligibilityView(BaseAPIView):
    '''
    API endpoint returning a list of eligible resources for a student

    /api/internal/student/[systemkey]/eligibility/
    '''
    def get(self, request, systemkey):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        if not valid_system_key(systemkey):
            return self.response_badrequest('Invalid systemkey')

        eligibilities = []
        try:
            student = StudentEligibility.objects.get(
                student__system_key=systemkey)
            for e in student.eligibility.all():
                if e.access_group == access_group:
                    eligibilities.append(EligibilityTypeSerializer(e).data)
        except StudentEligibility.DoesNotExist:
            pass

        return self.response_ok(eligibilities)

    def post(self, request, systemkey):
        if not valid_system_key(systemkey):
            return self.response_badrequest("Invalid systemkey")

        try:
            access_group = self.get_access_group(request)

            self.valid_user_override()

            eligibility_type_id = int(request.data.get("eligibility_type_id"))
            if eligibility_type_id < 0:
                return self.response_badrequest("Invalid TypeID")

            # update existing student record if one exists
            student = Student.objects.get(system_key=system_key)
            eligibility_type = EligibilityType.objects.get(
                id=eligibility_type_id, access_group=access_group)
            s_e, _ = StudentEligibility.objects.get_or_create(
                student=student)
            s_e.eligibility.add(eligibility_type)
            s_e.save()

            serializer = StudentEligibilitySerializer(s_e)
            logger.info(f"StudentEligibility for {system_key} saved: "
                        f"{serializer.data}")
            return self.response_ok(serializer.data)
        except Student.DoesNotExist:
            return self.response_notfound("Unknown student")
        except EligibilityType.DoesNotExist:
            return self.response_notfound("Unknown or unpermitted eligiblity")
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()
        except OverrideNotPermitted as err:
            return self.response_unauthorized(err)


class StudentCourseAnalyticsView(BaseAPIView):
    '''
    API endpoint returning a list of RAD analytics data for a specific
    student-course-term combination

    /api/internal/student/[uwnetid]/[year]/[quarter]/[course_id]
    '''
    def get(self, request, uwnetid, year, quarter, course_id):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        if not valid_uwnetid(uwnetid):
            return self.response_badrequest('Invalid uwnetid')

        rad_data = CourseAnalyticsScores.get_rad_data_for_course(year,
                                                                 quarter,
                                                                 uwnetid,
                                                                 course_id)
        response_json = [rad.json_data() for rad in rad_data]
        if len(response_json) == 0:
            return self.response_notfound()
        return self.response_ok(response_json)

class StudentSigninAnalyticsView(BaseAPIView):
    '''
    API endpoint returning a list of RAD analytics data for a specific
    student

    /api/internal/student/[uwnetid]/signins/
    '''
    def get(self, request, uwnetid):
        try:
            access_group = self.get_access_group(request)
        except AccessGroup.DoesNotExist:
            return self.response_unauthorized()

        if not valid_uwnetid(uwnetid):
            return self.response_badrequest('Invalid uwnetid')

        signin_data = (StudentSigninAnalytics.
                       get_signin_data_for_student(uwnetid))
        if len(signin_data) == 0:
            return self.response_notfound()
        return self.response_ok(signin_data)
