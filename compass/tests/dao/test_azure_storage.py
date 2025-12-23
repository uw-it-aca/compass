# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.test import TestCase
from compass.dao.azure_storage import AzureStorageDAO
from unittest.mock import patch


class TestAzureStorage(TestCase):
    def mock_init(self):
        pass

    def mock_list_blobs(self):
        sample_filenames = [
            'predictions/predictions_2025-05-19.csv',
            'predictions/predictions_2025-05-20.csv',
            'predictions/predictions_2025-05-27.csv',
            'predictions/predictions_2025-05-28.csv',
            'predictions/predictions_2025-06-11.csv',
            'predictions/predictions_2025-08-18.csv',
            'predictions/predictions_2025-08-25.csv',
            'predictions/odd_file.txt',
            'predictions/predictions_2025-12-22.csv',
            'predictions/predictions_2025-11-17.csv',
            'predictions/predictions_2025-11-24.csv',
            'predictions/predictions_2025-12-01.csv',
            'predictions/predictions_2025-12-08.csv',
            'predictions/predictions_2025-12-15.csv',
        ]
        return sample_filenames

    def mock_get_blob(self, blob_name):
        sample_contents = """
        ,system_key,student_no,uw_netid,yrq,course_code,pred
        0,0000001,1000001,javerage  ,20252,MATH 123 A,0.0
        1,0000002,1000002,jsmith    ,20252,BIOL 101 A,1.0
        2,0000003,1000003,adoe      ,20252,CHEM 105 A,0.0
        3,0000004,1000004,mbrown    ,20252,PHYS 121 A,1.0
        4,0000005,1000005,ljohnson  ,20252,ENGL 201 A,0.0
        5,0000006,1000006,kwilson   ,20252,HIST 110 A,1.0
        6,0000007,1000007,dperez    ,20252,PSYC 101 A,0.0
        7,0000008,1000008,sgarcia   ,20252,SOC 200 A,0.0
        8,0000009,1000009,tmiller   ,20252,ECON 101 A,1.0
        9,0000010,1000010,jbishop  ,20252,PHIL 101 A,1.0
        """
        return sample_contents

    @patch.multiple(AzureStorageDAO,
                    __init__=mock_init,
                    list_blob_names=mock_list_blobs)
    def test_get_latest_filename(self):
        dao = AzureStorageDAO()
        latest_filename = dao.get_most_recent_filename()
        self.assertEqual(latest_filename,
                         'predictions/predictions_2025-12-22.csv')

    @patch.multiple(AzureStorageDAO,
                    __init__=mock_init,
                    get_blob=mock_get_blob,
                    list_blob_names=mock_list_blobs)
    def test_get_latest_file(self):
        dao = AzureStorageDAO()
        latest_filename = dao.get_most_recent_filename()
        file_contents = dao.get_blob(latest_filename)
        self.assertIn('system_key,student_no,'
                      'uw_netid,yrq,course_code,pred',
                      file_contents)
        self.assertIn('0000001,1000001,javerage  ,'
                      '20252,MATH 123 A,0.0',
                      file_contents)
        self.assertIn('0000010,1000010,jbishop  ,'
                      '20252,PHIL 101 A,1.0',
                      file_contents)
