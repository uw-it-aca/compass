# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management.base import BaseCommand
from django.utils.text import slugify
from uw_person_client import UWPersonClient
from uw_person_client.exceptions import PersonNotFoundException
from uw_pws import PWS
from compass.models import (
    Contact, AppUser, AccessGroup, Student,
    ContactType, ContactMethod, ContactTopic)
from datetime import datetime
import argparse
import pytz
import sys
import csv
import re


class Command(BaseCommand):
    help = "load compass legacy data from csv dump of Appointment table"

    def add_arguments(self, parser):
        parser.add_argument('--start-id', type=int, default=None)
        parser.add_argument('--count', type=int, default=None)
        parser.add_argument('csvfile')

    def handle(self, *args, **options):
        self.uw_person = UWPersonClient()
        self.uw_pws = PWS()
        self.access_group = AccessGroup.objects.get(name='OMAD')
        self._student_syskey = {}

        # ignore IC (Instructional Center) contact types:
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
        #    Classroom Presentation
        #    Career Computer Lab
        excluded_re = re.compile('^(IC[- ].*'
                                 '|Classroom Presentation'
                                 '|Career Computer Lab)', re.I)

        n = 0
        count = options['count']
        start_id = options['start_id']
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

                if not excluded_re.match(appointment.Contact_Type):
                    self._create_contact(appointment)

                if count:
                    n += 1
                    if n >= count:
                        return

        self._sanitize_app_user()

    def _create_contact(self, apt):
        if int(apt.student_no) in self.unknown_student_ids:
            return

        student_number = apt.student_no.zfill(7)
        try:
            app_user = self._get_app_user(apt.staff_id, apt.staff_name)
            student = self._get_student(student_number)
            checkin_date = self._get_checkin_date(apt)
            trans_id = self._get_trans_id(apt)
            contact = Contact.objects.get(
                app_user=app_user, student=student, checkin_date=checkin_date)

            # add transaction id if not present
            if trans_id and not contact.trans_id:
                self._error("Contact gets trans_id {}".format(transid))
                contact.trans_id = trans_id
                contact.save()

            return
        except PersonNotFoundException:
            self.unknown_student_ids.add(int(apt.student_no))
            self._error("Appointment {}: student number {} not found".format(
                apt.ID, student_number))
            return
        except ValueError as ex:
            self._error("SKIP ID {}: {}".format(apt.ID, ex))
            return
        except Contact.DoesNotExist:
            # fall through to create new Contact
            pass

        self._error("Create Contact: {}, {}, {}".format(
            app_user, student, checkin_date))

        contact = Contact(
            app_user=app_user, student=student, checkin_date=checkin_date,
            contact_type=self._get_contact_type(apt.Contact_Type),
            contact_method=self._get_contact_method(apt),
            noshow=True if apt.NoShow.upper() == 'Y' else False,
            trans_id=trans_id, notes=apt.Notes,
            actions=apt.Actions, source=apt.Source)

        contact.save()

        self._add_contact_topics(apt, contact)
        self._add_access_group(contact)
        contact.save()

    def _get_app_user(self, netid, name):
        if (not netid) and name:
            try:
                last, first = name.split(',')
                person = self.uw_pws.person_search(
                    first_name=first.strip(), last_name=last.strip())
                if len(person) == 1:
                    netid = person[0].uwnetid
            except ValueError:
                pass

        app_user, created = AppUser.objects.get_or_create(uwnetid=netid)
        return app_user

    def _get_student(self, student_number):
        try:
            syskey = self._student_syskey[student_number]
        except KeyError:
            person = self.uw_person.get_person_by_student_number(
                student_number, include_employee=False, include_student=True,
                include_student_transcripts=False,
                include_student_transfers=False, include_student_sports=False,
                include_student_advisers=False, include_student_majors=False,
                include_student_pending_majors=False,
                include_student_holds=False, include_student_degrees=False)
            syskey = person.student.system_key
            self._student_syskey[student_number] = syskey

        student, created = Student.objects.get_or_create(system_key=syskey)
        return student

    def _get_checkin_date(self, apt):
        pacific = pytz.timezone('US/Pacific')
        naive_date = datetime.strptime(apt.Date, '%Y-%m-%d %H:%M:%S.%f')
        date = pacific.localize(naive_date)
        time = datetime.strptime(apt.Time_In, '%H:%M:%S')
        return date.replace(
            hour=time.hour,
            minute=time.minute,
            second=time.second).astimezone(pytz.utc)

    def _get_trans_id(self, apt):
        try:
            return int(apt.checkin_transid)
        except (ValueError, TypeError):
            pass

        return None

    def _get_contact_type(self, contact):
        mapping = [
            (re.compile('^Appointment$', re.I),
             'Appointment'),
            (re.compile('^Admin Notes$', re.I),
             'Admin'),
            (re.compile('^Notes$', re.I),
             'Advisor'),
            (re.compile('^(Event[/ ]Workshop'
                        '|ECC Meeting or Event'
                        '|ECC Event)$', re.I),
             'Event/Workshop')]

        if contact:
            for pat, name in mapping:
                if pat.search(contact):
                    return self._get_contact_type_model(name)

        return self._get_contact_type_model('Quick Question')

    def _get_contact_type_model(self, name):
        contact_type, created = ContactType.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slugify(name))

        return contact_type

    def _get_contact_method(self, apt):
        mapping = [
            (re.compile('^Telephone$', re.I),
             'Telephone'),
            (re.compile('^Notes$', re.I),
             'Internal'),
            (re.compile('^(Email Message'
                        '|Mass Email'
                        '|Email'
                        '|Email Contact)$', re.I),
             'E-mail')]

        if apt.Contact_Type:
            for pat, name in mapping:
                if pat.search(apt.Contact_Type):
                    return self._get_contact_method_model(name)

        # sniff notes for "Zoom" "A&O" and "A&R" indicating video contact
        if re.match(r'(Zoom|A&O|A&R)', apt.Notes, re.MULTILINE):
            return self._get_contact_method_model('Video Conference')

        return self._get_contact_method_model('In-Person')

    def _get_contact_method_model(self, name):
        contact_method, created = ContactMethod.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slugify(name))

        return contact_method

    def _add_contact_topics(self, apt, contact):
        mapping = [
            (re.compile('(Add/Drop Class|Academic Planning)', re.I),
             'Academic Planning & Changes'),
            (re.compile('Join/Affiliate', re.I),
             'Join/Affiliate'),
            (re.compile('Academic Difficulties', re.I),
             'Academic Difficulties'),
            (re.compile('Hardship Withdrawal', re.I),
             'FQD/CQD & S/NS'),
            (re.compile('(Internships|Research Opportunities'
                        '|Career Counselling[/]Advising)', re.I),
             'Internships, Research, and Career Exploration'),
            (re.compile('Graduate[/]Professional School', re.I),
             'Graduate & Professional School'),
            (re.compile('Study Abroad', re.I),
             'Study Abroad'),
            (re.compile('PreMajor Extension', re.I),
             'Pre-major Extension'),
            (re.compile('Reinstatement', re.I),
             'Reinstatement'),
            (re.compile('Personal Issues', re.I),
             'Personal Issues'),
            (re.compile('Financial Aid'),
             'Financial Aid'),
            (re.compile('(Test Assessment'
                        '|Referral-Campus/Community'
                        '|General ED Requirements'
                        '|Computer Lab'
                        '|Exit Interview'
                        '|Other)', re.I),
             'Other')]

        event_type = apt.Event_Type

        if event_type and not re.match('^[A-Za-z &]+ [0-9]+$', event_type):
            for pat, name in mapping:
                if pat.search(event_type):
                    topic = self._get_topic(name)
                    contact.contact_topics.add(topic)

        # sniff at Appointment for other cues
        if apt.PersonalFamilyIssues in ['1', 1]:
            topic = self._get_topic('Personal Issues')
            contact.contact_topics.add(topic)

        if apt.Contact_Type and apt.Contact_Type == 'Notes':
            contact.contact_topics.add(self._get_topic('Other'))

    def _get_topic(self, name):
        topic, created = ContactTopic.objects.get_or_create(
            access_group=self.access_group, name=name, slug=slugify(name))

        return topic

    def _sanitize_app_user(self):
        prior_netids = []
        for app_user in AppUser.objects.all():
            if not self.uw_pws.valid_uwnetid(app_user.uwnetid):
                self._error(
                    "Person {}: invalid netid".format(app_user.uwnetid))
                continue

            try:
                person = self.uw_person.get_person_by_uwnetid(app_user.uwnetid)
            except PersonNotFoundException:
                self._error("Person {}: not found".format(app_user.uwnetid))
                continue

            for prior_netid in person.prior_uwnetids:
                try:
                    if app_user.uwnetid == prior_netid:
                        continue

                    prior_app_user = AppUser.objects.get(uwnetid=prior_netid)
                    contacts = Contact.objects.filter(app_user=prior_app_user)
                    self._error("Update {} contacts from {} to {}".format(
                        contacts.count(), prior_app_user, app_user))
                    contacts.update(app_user=app_user)
                    prior_netids.append(prior_app_user.uwnetid)
                except AppUser.DoesNotExist:
                    pass

        for netid in prior_netids:
            app_user = AppUser.objects.get(uwnetid=netid)
            self._error("Deleting AppUser {}".format(app_user))
            app_user.delete()

    def _add_access_group(self, contact):
        contact.access_group.add(self.access_group)

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
