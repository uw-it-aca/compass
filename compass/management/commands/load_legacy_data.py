# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from uw_person_client import UWPersonClient
from compass.models import (
    Contact, AppUser, AccessGroup, Student,
    ContactType, ContactMethod, ContactTopic)
from datetime import datetime
from pytz import timezone
import argparse
import pytz
import sys
import csv
import re


class Command(BaseCommand):
    help = "load compass legacy data from csv dump of Appointment table"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, nargs='?', default=None)
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)

    def handle(self, *args, **options):
        self.uw_person = UWPersonClient()
        self.access_group = AccessGroup.objects.get(name='OMAD')

        n = 0
        count = options['count']
        first_line = True
        for row in csv.reader(options['infile'], delimiter=","):
            if first_line:
                first_line = False
                continue

            try:
                self._create_contact(Appointment(row))
                if count:
                    n += 1
                    if n >= count:
                        return
            except Exception as ex:
                print("FAILED ROW {}: {}".format(row.ID, ex))

    def _create_contact(self, apt):
        try:
            app_user = self._get_app_user(apt.staff_id)
            student = self._get_student(apt.student_number)
            checkin_date = self._get_checkin_date(apt)
            Contact.objects.get(
                app_user=app_user, student=student, checkin_date=checkin_date)
            return
        except ValueError as ex:
            print("SKIP ID {}: {}".format(apt.ID, ex), file=sys.stderr)
            return
        except Contact.DoesNotExist:
            # fall through to create new Contact
            pass

        contact = Contact(
            app_user=app_user, student=student, checkin_date=checkin_date,
            contact_type=self._get_contact_type(apt.Contact_Type),
            contact_method=self._get_contact_method(apt),
            noshow=True if apt.NoShow.upper() == 'Y' else False,
            notes=apt.Notes, actions=apt.Actions, source=apt.Source)
            
        contact.save()

        self._add_contact_topics(apt, contact)
        self._add_access_group(contact)
        contact.save()

    def _get_app_user(self, netid):
        app_user, created = AppUser.objects.get_or_create(uwnetid=netid)
        return app_user

    def _get_student(self, student_number):
        person = self.uw_person.get_person_by_student_number(
            student_number, include_student=True)
        student, created = Student.objects.get_or_create(
            person.student.system_key)

        # if created:
        #     raise Exception('wire up programs')

        return student

    def _get_checkin_date(self, apt):
        pacific = timezone('US/Pacific')
        naive_date = datetime.strptime(apt.Date, '%Y-%m-%d %H:%M:%S.%f')
        date = pacific.localize(naive_date)
        time = datetime.strptime(apt.Time_In, '%H:%M:%S')
        return date.replace(
            hour=time.hour, minute=time.minute, second=time.second)

    def _get_contact_type(self, contact):
        mapping = [
            (re.compile('Appointment', re.I),
             'Appointment',
             'appointment'),
            (re.compile('Admin Notes', re.I),
             'Admin',
             'admin'),
            (re.compile('(Workshop'
                        '|ECC Meeting or Event'
                        '|ECC Event)', re.I),
             'Event Workshop',
             'event-workshop')]

        if contact:
            for pat, name, slug in mapping:
                if pat.search(contact):
                    return self._get_contact_type_model(name, slug)

        return self._get_contact_type_model('Quick Question', 'quick-question')

    def _get_contact_type_model(self, name, slug):
        contact_type, created = ContactType.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slug)
        return contact_type

    def _get_contact_method(self, apt):
        mapping = [
            (re.compile('Telephone', re.I),
             'Telephone',
             'telephone'),
            (re.compile('(Email Message'
                        '|Mass Email'
                        '|Email'
                        '|Email Contact)', re.I),
             'E-mail',
             'e-mail')]

        if apt.Contact_Type:
            for pat, name, slug in mapping:
                if pat.search(apt.Contact_Type):
                    return self._get_contact_method_model(name, slug)

        # sniff notes for "Zoom" "A&O" and "A&R" indicating video contact
        if re.match(r'(Zoom|A&O|A&R)', apt.Notes, re.MULTILINE):
            return self._get_contact_method_model(
                'Video Conference', 'video-conference')

        return self._get_contact_method_model('In Person', 'in-person')

    def _get_contact_method_model(self, name, slug):
        contact_method, created = ContactMethod.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slug)
        return contact_method

    def _add_contact_topics(self, apt, contact):
        mapping = [
            (re.compile('(Add\/Drop Class|Academic Planning)', re.I),
             'Academic Planning & Changes',
             'academic-planning-changes'),
            (re.compile('Join\/Affiliate', re.I),
             'Join/Affiliate',
             'joinaffiliate'),
            (re.compile('Academic Difficulties', re.I),
             'Academic Difficulties',
             'academic-difficulties'),
            (re.compile('Hardship Withdrawal', re.I),
             'FQD/CQD & S/NS',
             'fqdcqd-sns'),
            (re.compile('(Internships|Research Opportunities'
                        '|Career Counselling/Advising)', re.I),
             'Internships, Research, and Career Exploration',
             'internships-research-career-exploration'),
            (re.compile('Graduate/Professional School', re.I),
             'Graduate & Professional School',
             'graduateprofessional-school'),
            (re.compile('Study Abroad', re.I),
             'Study Abroad',
             'study-abroad'),
            (re.compile('PreMajor Extension', re.I),
             'Pre-major Extension',
             'pre-major-extension'),
            (re.compile('Reinstatement', re.I),
             'Reinstatement',
             'reinstatement'),
            (re.compile('Personal Issues', re.I),
             'Personal Issues',
             'personal-issues'),
            (re.compile('Financial Aid'),
             'Financial Aid',
             'financial-aid'),
            (re.compile('(Test Assessment'
                        '|Referral-Campus/Community'
                        '|General ED Requirements'
                        '|Computer Lab'
                        '|Exit Interview'
                        '|Other)', re.I),
             'Other',
             'other')]

        event_type = apt.Event_Type

        if event_type and not re.match('^[A-Za-z &]+ [0-9]+$', event_type):
            for pat, name, slug in mapping:
                if pat.search(event_type):
                    topic = self._get_topic(name, slug)
                    contact.event_type.add(topic)

        # sniff at Appointment for other cues
        if apt.PersonalFamilyIssues in ['1', 1]:
            topic = self._get_topic('Personal Issues', 'personal-issues')
            contact.event_type.add(topic)

    def _get_topic(self, name, slug):
        topic, created = ContactTopic.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slug)

        return topic

    def _add_access_group(self, contact):
        contact.access_group.add(self.access_group)


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
            setattr(self, k, row[i])
