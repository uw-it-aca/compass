# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from compass.tests import CompassTestCase
from compass.dao.compass_visits import (get_visits_for_student,
                                        get_admin_visit_list,
                                        get_visit_options,
                                        admin_create_visit,
                                        admin_update_visit,
                                        admin_delete_visit)
from uw_compass_visits.models import Visit
from restclients_core.exceptions import DataFailureException
import datetime


class CompassVisitsDaoTest(CompassTestCase):
    def test_visits_for_student(self):
        visits = get_visits_for_student("javerage")
        self.assertIsNotNone(visits)
        self.assertEqual(len(visits), 2)
        self.assertEqual(visits[0].id, 1)
        self.assertEqual(visits[0].student_netid, "javerage")
        self.assertEqual(visits[0].program_area, "Program Area 3")

        visits = get_visits_for_student("jnovisits")
        self.assertIsNotNone(visits)
        self.assertEqual(len(visits), 0)

    def test_get_admin_visit_list(self):
        visits = get_admin_visit_list()
        self.assertIsNotNone(visits)
        self.assertEqual(len(visits['pending_verification']), 2)
        self.assertEqual(len(visits['by_programarea']), 2)
        self.assertEqual(len(visits['by_programarea']['Program Area 2']), 1)
        self.assertEqual(len(visits['by_programarea']['Program Area 3']), 2)

    def test_get_visit_options(self):
        options = get_visit_options()
        self.assertIsNotNone(options)
        self.assertIn('program_areas', options)
        self.assertIn('tutoring_options', options)
        self.assertIn('writing_services', options)
        self.assertEqual(len(options['program_areas']), 4)
        self.assertEqual(len(options['tutoring_options']), 3)
        self.assertEqual(len(options['writing_services']), 2)
        self.assertEqual(options['program_areas'][0]['id'], 1)
        self.assertEqual(options['program_areas'][0]['name'],
                         'Program Area 1')

    def test_admin_create_visit(self):
        visit = Visit(id=6,
                      student_netid="jnewvisit",
                      program_area="Program Area 1",
                      check_in_date=datetime.datetime(2022, 9, 19, 6, 15, 4),
                      is_verified=False)
        with self.assertRaises(DataFailureException):
            # will fail because the mock dao doesn't support creating visits
            admin_create_visit(visit)

    def test_admin_update_visit(self):
        visit = admin_update_visit(1)
        self.assertIsNotNone(visit)
        self.assertEqual(visit.id, 1)

        with self.assertRaises(DataFailureException):
            admin_update_visit(999)

    def test_admin_delete_visit(self):
        response = admin_delete_visit(1)
        self.assertIsNotNone(response)
        self.assertEqual(response.status, 200)

        with self.assertRaises(DataFailureException):
            admin_delete_visit(999)
