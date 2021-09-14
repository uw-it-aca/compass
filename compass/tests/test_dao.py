# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import pandas as pd
import unittest
from django.test import TestCase
from compass.dao import EdwDAO, SwsDAO
from mock import call, patch, MagicMock


class TestSwsDAO(TestCase):

    def get_test_sws_dao(self):
        sws_dao = SwsDAO()
        return sws_dao

    def mock_get_or_create_from_sws_term(self, sws_term):
        term = MagicMock()
        term.sis_term_id = sws_term.sis_term_id
        return term, True

    @patch('compass.dao.Term')
    def test_create_terms(self, mock_term_model):
        td = self.get_test_sws_dao()
        mock_term1 = MagicMock()
        mock_term1.sis_term_id = "2021-spring"
        mock_term2 = MagicMock()
        mock_term2.sis_term_id = "2021-summer"
        mock_terms = [mock_term1, mock_term2]
        td.get_sws_terms = MagicMock(return_value=mock_terms)
        mock_term_model.objects.get_or_create_from_sws_term = \
            MagicMock(side_effect=self.mock_get_or_create_from_sws_term)
        td.create_terms()
        call_args_list = (
            mock_term_model.objects.get_or_create_from_sws_term
            .call_args_list)
        assert (call_args_list[0] == call(mock_term1))
        assert (call_args_list[1] == call(mock_term2))
        self.assertEqual(len(call_args_list), 2)


class TestEdwDAO(TestCase):

    def _get_test_edw_dao(self):
        edw = EdwDAO()
        edw.get_connection = MagicMock()
        return edw

    @patch('compass.dao.pd.read_sql')
    def _get_mock_enrolled_students_df(self, mock_read_sql):
        edw_dao = self._get_test_edw_dao()
        mock_enrolled_students_file = \
            os.path.join(
                os.path.dirname(__file__),
                'test_data/enrolled_students.csv')
        mock_read_sql.return_value = \
            pd.read_csv(mock_enrolled_students_file, sep=",")
        mock_enrolled_students_df = \
            edw_dao.get_enrolled_students_df()
        return mock_enrolled_students_df

    @patch('compass.dao.pymssql.connect')
    @patch('compass.dao.settings')
    def test_get_connection(self, mock_settings, mock_pymssql_connect):
        mock_database = MagicMock()
        mock_settings.EDW_PASSWORD = MagicMock()
        mock_settings.EDW_USERNAME = MagicMock()
        mock_settings.EDW_HOSTNAME = MagicMock()
        edw = EdwDAO()
        conn = edw.get_connection(mock_database)
        mock_pymssql_connect.assert_called_once_with(
            mock_settings.EDW_HOSTNAME,
            mock_settings.EDW_USERNAME,
            mock_settings.EDW_PASSWORD,
            mock_database)
        self.assertEqual(conn, mock_pymssql_connect.return_value)

    def test_get_enrolled_students_df(self):
        mock_enrolled_students_df = self._get_mock_enrolled_students_df()
        self.assertEqual(
            mock_enrolled_students_df.columns.values.tolist(),
            ["SystemKey", "StudentNumber", "UWNetID", "StudentName",
             "StudentNamePreferredFirst", "StudentNamePreferredMiddle",
             "StudentNamePreferredLast", "BirthDate", "StudentEmail",
             "ExternalEmail", "LocalPhoneNumber", "Gender", "GPA",
             "TotalCredits", "Major1", "Major2", "Major3", "Minor1", "Minor2",
             "Minor3", "CampusDesc"])


if __name__ == "__main__":
    unittest.main()
