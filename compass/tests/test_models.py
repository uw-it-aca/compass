# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest
from django.test import TestCase
from compass.models import Term
from mock import MagicMock, patch


class TestTermManager(TestCase):

    def setUp(self):
        self.mock_get_current_term = \
            self.create_patch('compass.models.get_current_term')
        self.mock_get_term_by_year_and_quarter = self.create_patch(
            'compass.models.get_term_by_year_and_quarter')
        self.mock_get_or_create_from_sws_term = self.create_patch(
            'compass.models.TermManager.get_or_create_from_sws_term')

    def restart_all(self):
        self.mock_get_current_term.reset_mock()
        self.mock_get_or_create_from_sws_term.reset_mock()
        self.mock_get_term_by_year_and_quarter.reset_mock()

    def create_patch(self, name):
        patcher = patch(name)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def test_get_or_create_term_from_sis_term_id(self):

        # assert call sequence when NO sis_term_id is supplied and there is
        # no existing term for the current date does NOT EXIST
        Term.objects.get_term_for_date = MagicMock(return_value=None)
        Term.objects.get_or_create_term_from_sis_term_id()
        self.assertTrue(Term.objects.get_term_for_date.called)
        self.assertTrue(self.mock_get_current_term.called)
        self.assertFalse(self.mock_get_term_by_year_and_quarter.called)
        self.assertTrue(self.mock_get_or_create_from_sws_term.called)

        self.restart_all()

        # assert call sequence when NO sis_term_id is supplied and
        # an existing term for the current date EXISTS
        mock_existing_term = MagicMock()
        Term.objects.get_term_for_date = \
            MagicMock(return_value=mock_existing_term)
        term, created = Term.objects.get_or_create_term_from_sis_term_id()
        self.assertTrue(Term.objects.get_term_for_date.called)
        self.assertFalse(self.mock_get_current_term.called)
        self.assertFalse(self.mock_get_term_by_year_and_quarter.called)
        self.assertFalse(self.mock_get_or_create_from_sws_term.called)
        self.assertEqual((term, created), (mock_existing_term, False))

        self.restart_all()

        # assert call sequence when sis_term_id is supplied
        Term.objects.get_term_for_date = MagicMock(return_value=None)
        Term.objects.get_or_create_term_from_sis_term_id(
                                                    sis_term_id="2021-spring")
        self.assertFalse(Term.objects.get_term_for_date.called)
        self.assertFalse(self.mock_get_current_term.called)
        self.assertTrue(self.mock_get_term_by_year_and_quarter.called)
        self.assertTrue(self.mock_get_or_create_from_sws_term.called)


if __name__ == "__main__":
    unittest.main()
