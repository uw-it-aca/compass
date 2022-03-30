# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import unittest
from django.test import TestCase
from compass.dao import SwsDAO
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


if __name__ == "__main__":
    unittest.main()
