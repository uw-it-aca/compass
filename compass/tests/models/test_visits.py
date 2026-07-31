# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime, timezone

from compass.models import AccessGroup, Student, Visit, VisitTutoringOption, VisitType
from compass.tests import CompassTestCase


class VisitModelTest(CompassTestCase):
    def setUp(self):
        super().setUp()
        self.student = Student(system_key="123456789")
        self.student.save()
        self.access_group = AccessGroup(
            name="Test Group", access_group_id="test_group")
        self.access_group.save()
        self.visit_type = VisitType(name="Test Visit Type",
                                    slug="test_visit_type",
                                    access_group=self.access_group)
        self.visit_type.save()
        self.tutoring_option = \
            VisitTutoringOption(name="Test Tutoring Option",
                                slug="test_tutoring_option",
                                access_group=self.access_group)
        self.tutoring_option.save()

    def test_get_cur_qtr(self):
        # mock current quarter first day is 2020-09-30
        cur_term_date = datetime(2020, 10, 1, tzinfo=timezone.utc)
        last_year = cur_term_date.replace(year=cur_term_date.year - 1)
        visit1 = Visit(student=self.student,
                       visit_type=self.visit_type,
                       tutoring_option=self.tutoring_option,
                       checkin_date=last_year,
                       checkout_date=last_year,
                       access_group=self.access_group
                       )
        visit1.save()
        visit2 = Visit(student=self.student,
                       visit_type=self.visit_type,
                       tutoring_option=self.tutoring_option,
                       checkin_date=cur_term_date,
                       checkout_date=cur_term_date,
                       access_group=self.access_group
                       )
        visit2.save()

        current_quarter_visits = \
            Visit.get_current_quarter_visits_by_student_syskey(
                self.student.system_key)
        self.assertEqual(len(current_quarter_visits), 1)
