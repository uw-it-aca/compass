# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.core.management import call_command
from compass.tests import CompassTestCase
from compass.models import Contact, Student, StudentAffiliation, \
    Visit, StudentEligibility, Affiliation, Cohort, AccessGroup, AppUser, \
    ContactType, ContactMethod, EligibilityType
from datetime import datetime
import pytz


class TestFixSyskey(CompassTestCase):
    student_pad = None
    student_nopad = None
    student_onlypad = None
    student_nodata = None
    contact_pad = None
    contact_nopad = None
    visit_pad = None
    visit_nopad = None
    elig_pad = None
    elig_nopad = None
    ag = None
    affil = None
    cohort = None
    appUser = None
    ctype = None
    cmeth = None
    et = None

    def setUp(self):
        # Required base data
        self.ag = AccessGroup(name="OMAD", access_group_id="u_astra_group1")
        self.ag.save()

        self.affil = Affiliation.objects.create(access_group=self.ag,
                                                name="test",
                                                slug="test")
        self.affil.save()

        self.cohort = Cohort.objects.create(start_year=2020,
                                            end_year=2021)
        self.cohort.save()

        self.appUser = AppUser.objects.create(uwnetid='testuser')
        self.appUser.save()

        self.ctype = ContactType.objects.create(access_group=self.ag,
                                                name="test",
                                                slug="test")
        self.ctype.save()

        self.cmeth = ContactMethod.objects.create(access_group=self.ag,
                                                  name="test",
                                                  slug="test")
        self.cmeth.save()

        self.etype = EligibilityType.objects.create(access_group=self.ag,
                                                    name="test",
                                                    slug="test")

        # Student Specific data
        self.student_pad = Student.objects.create(system_key='001234567')
        self.student_pad.save()
        self.student_nopad = Student.objects.create(system_key='1234567')
        self.student_nopad.save()
        self.student_onlypad = Student.objects.create(system_key='7654321')
        self.student_nopad.save()
        self.student_nodata = Student.objects.create(system_key='3513985')
        self.student_nodata.save()

        self.contact_pad = Contact.objects \
            .create(app_user=self.appUser,
                    student=self.student_pad,
                    contact_type=self.ctype,
                    contact_method=self.cmeth,
                    checkin_date=datetime.now(pytz.utc)
                    )
        self.contact_pad.save()
        self.contact_pad.access_group.set([self.ag])

        self.contact_nopad = Contact.objects \
            .create(app_user=self.appUser,
                    student=self.student_nopad,
                    contact_type=self.ctype,
                    contact_method=self.cmeth,
                    checkin_date=datetime.now(pytz.utc)
                    )
        self.contact_nopad.save()
        self.contact_nopad.access_group.set([self.ag])
        self.contact_onlypad = Contact.objects \
            .create(app_user=self.appUser,
                    student=self.student_onlypad,
                    contact_type=self.ctype,
                    contact_method=self.cmeth,
                    checkin_date=datetime.now(pytz.utc)
                    )
        self.contact_onlypad.save()
        self.contact_onlypad.access_group.set([self.ag])

        self.affil_pad = StudentAffiliation.objects \
            .create(student=self.student_pad,
                    affiliation=self.affil)
        self.affil_pad.save()
        self.affil_pad.cohorts.set([self.cohort])

        self.affil_nopad = StudentAffiliation.objects \
            .create(student=self.student_nopad,
                    affiliation=self.affil)
        self.affil_nopad.save()
        self.affil_nopad.cohorts.set([self.cohort])

        self.affil_onlypad = StudentAffiliation.objects \
            .create(student=self.student_onlypad,
                    affiliation=self.affil)
        self.affil_onlypad.save()
        self.affil_onlypad.cohorts.set([self.cohort])

        self.visit_pad = Visit.objects \
            .create(student=self.student_pad,
                    access_group=self.ag,
                    course_code="asdf",
                    checkin_date=datetime.now(pytz.utc),
                    checkout_date=datetime.now(pytz.utc))
        self.visit_pad.save()

        self.visit_nopad = Visit.objects \
            .create(student=self.student_nopad,
                    access_group=self.ag,
                    course_code="asdf",
                    checkin_date=datetime.now(pytz.utc),
                    checkout_date=datetime.now(pytz.utc))
        self.visit_nopad.save()
        self.visit_onlypad = Visit.objects \
            .create(student=self.student_onlypad,
                    access_group=self.ag,
                    course_code="asdf",
                    checkin_date=datetime.now(pytz.utc),
                    checkout_date=datetime.now(pytz.utc))
        self.visit_onlypad.save()

        self.elig_pad = StudentEligibility.objects \
            .create(student=self.student_pad)
        self.elig_pad.save()
        self.elig_pad.eligibility.set([self.etype])

        self.elig_nopad = StudentEligibility.objects \
            .create(student=self.student_nopad)
        self.elig_nopad.save()
        self.elig_nopad.eligibility.set([self.etype])

        self.elig_onlypad = StudentEligibility.objects \
            .create(student=self.student_onlypad)
        self.elig_onlypad.save()
        self.elig_onlypad.eligibility.set([self.etype])

    def test_fix(self):
        # Verify dupe students exist
        self.assertEqual(len(Student.objects.all()), 4)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='001234567')),
            1)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='1234567')),
            1)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='7654321')),
            1)
        self.assertEqual(len(
            StudentAffiliation.objects
            .filter(student__system_key='001234567')),
            1)
        self.assertEqual(len(
            StudentAffiliation.objects.filter(student__system_key='1234567')),
            1)
        self.assertEqual(len(
            StudentAffiliation.objects.filter(student__system_key='7654321')),
            1)
        self.assertEqual(len(
            Visit.objects.filter(student__system_key='001234567')),
            1)
        self.assertEqual(len(
            Visit.objects.filter(student__system_key='1234567')),
            1)
        self.assertEqual(len(
            Visit.objects.filter(student__system_key='7654321')),
            1)
        self.assertEqual(len(
            StudentEligibility.objects
            .filter(student__system_key='001234567')),
            1)
        self.assertEqual(len(
            StudentEligibility.objects
            .filter(student__system_key='001234567')),
            1)
        self.assertEqual(len(
            StudentEligibility.objects.filter(student__system_key='7654321')),
            1)

        # Fix dupes
        call_command('fix_student_syskey_padding')

        # Verify dupes are merged
        self.assertEqual(len(Student.objects.all()), 3)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='001234567')),
            2)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='1234567')),
            0)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='7654321')),
            0)
        self.assertEqual(len(
            Contact.objects.filter(student__system_key='007654321')),
            1)

        self.assertEqual(len(
            StudentAffiliation.objects.
            filter(student__system_key='001234567')),
            2)
        self.assertEqual(len(
            StudentAffiliation.objects.filter(student__system_key='1234567')),
            0)
        self.assertEqual(len(
            StudentAffiliation.objects.filter(student__system_key='7654321')),
            0)
        self.assertEqual(len(
            StudentAffiliation.objects
            .filter(student__system_key='007654321')),
            1)

        self.assertEqual(len(
            Visit.objects.filter(student__system_key='001234567')),
            2)
        self.assertEqual(len(
            Visit.objects.filter(student__system_key='1234567')),
            0)
        self.assertEqual(len(
            Visit.objects.filter(student__system_key='7654321')),
            0)
        self.assertEqual(len(
            Visit.objects.filter(student__system_key='007654321')),
            1)

        self.assertEqual(len(
            StudentEligibility.objects.
            filter(student__system_key='001234567')),
            2)
        self.assertEqual(len(
            StudentEligibility.objects.filter(student__system_key='1234567')),
            0)
        self.assertEqual(len(
            StudentEligibility.objects.filter(student__system_key='7654321')),
            0)
        self.assertEqual(len(
            StudentEligibility.objects
            .filter(student__system_key='007654321')),
            1)
