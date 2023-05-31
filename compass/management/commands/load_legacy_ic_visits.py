# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.utils.text import slugify
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
from compass.models import Student, Visit, VisitType, AccessGroup
from datetime import datetime
from pytz import timezone
import sys
import csv
import re


class Command(BaseCommand):
    help = "load compass legacy IC visits from csv dump of Appointment table"

    def add_arguments(self, parser):
        parser.add_argument('--start-id', type=int, default=None)
        parser.add_argument('--count', type=int, default=None)
        parser.add_argument('csvfile')

    def handle(self, *args, **options):
        self.uw_person = UWPersonClient()
        self.access_group = AccessGroup.objects.get(name='OMAD')

        # include IC (Instructional Center) contact types:
        #    IC Drop-In Tutoring
        #    IC Exam Prep
        #    IC-Exam Prep (Workshop)
        #    IC-Writing
        #    IC-Exam Prep (Drop-In)
        #    IC-Read/Study Skill
        #    IC Writing Assistance
        #    IC-Tutoring (Workshop)
        #    IC-Tutoring (Drop-In)
        #    IC Computer Usage
        #    IC-Computer Lab
        #    IC Workshop
        ic_re = re.compile('^IC[- ].*', re.I)

        n = 0
        count = options['count']
        start_id = options['start_id']
        self.student_syskey = {}
        self.unknown_student_ids = set()
        with open(options['csvfile']) as csvfile:
            next(csvfile, None)
            for row in csv.reader(csvfile, delimiter=","):
                appointment = Appointment(row)
                if start_id:
                    if start_id == int(appointment.ID):
                        start_id = None
                    else:
                        continue

                if ic_re.match(appointment.Contact_Type):
                    self._create_visit(appointment)

                if count:
                    n += 1
                    if n >= count:
                        return

    def _create_visit(self, apt):
        if int(apt.student_no) in self.unknown_student_ids:
            return

        student_number = apt.student_no.zfill(7)
        try:
            student = self._get_student(student_number)
            checkin_date = self._get_checkin_date(apt)
            checkout_date = self._get_checkout_date(apt)
            Visit.objects.get(
                student=student, checkin_date=checkin_date,
                checkout_date=checkout_date)
            return
        except PersonNotFoundException:
            self.unknown_student_ids.add(int(apt.student_no))
            self._error("IC Visit {}: student number {} not found".format(
                apt.ID, student_number))
            return
        except ValueError as ex:
            self._error("SKIP ID {}: {}".format(apt.ID, ex))
            return
        except Visit.DoesNotExist:
            # fall through to create new Visit
            pass

        visit = Visit(
            access_group=self.access_group, student=student, ic_eligible=True,
            checkin_date=checkin_date, checkout_date=checkout_date,
            course_code=self._get_course_code(apt),
            visit_type=self._get_visit_type(apt))

        visit.save()

    def _get_student(self, student_number):
        try:
            syskey = self.student_syskey[student_number]
        except KeyError:
            person = self.uw_person.get_person_by_student_number(
                student_number, include_employee=False, include_student=True,
                include_student_transcripts=False,
                include_student_transfers=False, include_student_sports=False,
                include_student_advisers=False, include_student_majors=False,
                include_student_pending_majors=False,
                include_student_holds=False, include_student_degrees=False)
            syskey = person.student.system_key
            self.student_syskey[student_number] = syskey

        student, created = Student.objects.get_or_create(system_key=syskey)
        return student

    def _get_checkin_date(self, apt):
        pacific = timezone('US/Pacific')
        naive_date = datetime.strptime(apt.Date, '%Y-%m-%d %H:%M:%S.%f')
        date = pacific.localize(naive_date)
        time = datetime.strptime(apt.Time_In, '%H:%M:%S')
        return date.replace(
            hour=time.hour, minute=time.minute, second=time.second)

    def _get_checkout_date(self, apt):
        pacific = timezone('US/Pacific')
        naive_date = datetime.strptime(apt.Date, '%Y-%m-%d %H:%M:%S.%f')
        date = pacific.localize(naive_date)
        time = datetime.strptime(apt.Time_Out, '%H:%M:%S')
        return date.replace(
            hour=time.hour, minute=time.minute, second=time.second)

    def _get_course_code(self, apt):
        return apt.Event_Type or "None"

    def _get_visit_type(self, apt):
        return self._get_visit_type_model(apt.Contact_Type)

    def _get_visit_type_model(self, name):
        visit_type, created = VisitType.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slugify(name))

        return visit_type

    def _error(self, msg):
        print(msg, file=sys.stderr)



class Appointment(object):
    APPOINTMENT_COLUMNS = [
        "ID",
        "student_no",
        "staff_id",
        "staff_name",
        "Contact_Type",
        "Date",
        "Time_In",
        "Time_Out",
        "Appt_Mins",
        "AddDropclass",
        "JoinAffiliate",
        "AcademicDifficulties",
        "HardshipWithdrawl",
        "Internship",
        "ResearchOpportunities",
        "GraduateProfessionalSchoolA",
        "TestingAssessments",
        "StudyAbroad",
        "CareerCounselingAdvising",
        "AcademicPlanningProgress",
        "PremajorExtension",
        "ReferralCampusCommunity",
        "ComputerLab",
        "ExitInterview",
        "Reinstatement",
        "FinancialAid",
        "GenderEdReq",
        "PersonalFamilyIssues",
        "Other",
        "NoShow",
        "Notes",
        "Actions",
        "Follow_Up_Date",
        "Follow_Up_Complete",
        "From",
        "To",
        "Subject",
        "CC",
        "BCC",
        "Attachment",
        "Add_Email_To_Record",
        "logged",
        "Event_Type",
        "Class",
        "GPA",
        "Source",
        "PriMaj",
        "quarter",
        "Year",
        "Program_Area",
        "credits",
        "TimeDateOut",
        "TimeDateIn",
        "AutoLogOut",
        "DataFix",
        "EOP",
        "DBNotes",
        "checkin_transid"]

    def __init__(self, row):
        for i, k in enumerate(self.APPOINTMENT_COLUMNS):
            setattr(self, k, row[i].strip())
