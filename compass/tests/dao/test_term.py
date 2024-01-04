# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from uw_sws.util import fdao_sws_override
from compass.dao.term import *


@fdao_sws_override
class TermDAOFunctionsTest(TestCase):
    def test_current_term(self):
        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-10-15 00:00:00'):
            term = current_term()
            self.assertEqual(term.year, 2013)
            self.assertEqual(term.quarter, 'autumn')

    def test_term_context(self):
        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-10-15 00:00:00'):
            self.assertEqual(term_context(), {
                'aterm_last_day': None,
                'break_term_quarter': 'autumn',
                'break_term_year': 2013,
                'bterm_first_day': None,
                'current_date': '2013-10-15',
                'current_term_quarter': 'autumn',
                'current_term_year': 2013,
                'is_break': False,
                'is_finals': False,
                'last_final_exam_date': '2013-12-13',
                'next_term_quarter': 'winter',
                'next_term_year': 2014,
                'term_first_day': '2013-09-25',
                'term_last_day': '2013-12-06',
                'term_week': 3,
            })

        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-12-23 00:00:00'):
            self.assertEqual(term_context(), {
                'aterm_last_day': None,
                'break_term_quarter': 'winter',
                'break_term_year': 2014,
                'bterm_first_day': None,
                'current_date': '2013-12-23',
                'current_term_quarter': 'autumn',
                'current_term_year': 2013,
                'is_break': True,
                'is_finals': False,
                'last_final_exam_date': '2013-12-13',
                'next_term_quarter': 'winter',
                'next_term_year': 2014,
                'term_first_day': '2013-09-25',
                'term_last_day': '2013-12-06',
                'term_week': 13,
            })

        with self.settings(CURRENT_DATETIME_OVERRIDE='2013-06-30 00:00:00'):
            self.assertEqual(term_context(), {
                'aterm_last_day': '2013-07-24',
                'break_term_quarter': 'summer',
                'break_term_year': 2013,
                'bterm_first_day': '2013-07-25',
                'current_date': '2013-06-30',
                'current_term_quarter': 'summer',
                'current_term_year': 2013,
                'is_break': False,
                'is_finals': False,
                'last_final_exam_date': '2013-08-23',
                'next_term_quarter': 'autumn',
                'next_term_year': 2013,
                'term_first_day': '2013-06-24',
                'term_last_day': '2013-08-23',
                'term_week': 1,
            })
