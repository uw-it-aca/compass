# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.tests import ApiTest
from compass.dao.photo import PhotoDAO
from mock import patch


class PhotoAPITest(ApiTest):
    def test_get(self):
        response = self.get_response(
            "photo", "javerage", kwargs={
                "uwregid": "9136CCB8F66711D5BE060004AC494FFE",
                "photo_key": "1234567812345678"})
        self.assertEqual(response.status_code, 404, "Not found")

        key = PhotoDAO().generate_photo_key()
        response = self.get_response(
            "photo", "javerage", kwargs={
                "uwregid": "9136CCB8F66711D5BE060004AC494FFE",
                "photo_key": key})
        self.assertEqual(response.status_code, 200, "OK")
        self.assertEqual(response.headers["Content-Type"], "image/jpeg")
