# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.apps import AppConfig
from restclients_core.dao import MockDAO
from uw_person_client.clients.mock_client import MockedUWPersonClient
import os


class CompassConfig(AppConfig):
    name = 'compass'

    def ready(self):
        restclient_mocks = os.path.join(os.path.dirname(__file__),
                                        "resources")
        MockDAO.register_mock_path(restclient_mocks)
        pds_mocks = os.path.join(os.path.dirname(__file__),
                                 "fixtures/mock_pds_data")
        MockedUWPersonClient.register_mock_path(pds_mocks)
