# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.apps import AppConfig
from restclients_core.dao import MockDAO
import os


class CompassConfig(AppConfig):
    name = 'compass'

    def ready(self):
        cohort_manager_mocks = os.path.join(os.path.dirname(__file__),
                                            "resources")
        MockDAO.register_mock_path(cohort_manager_mocks)
