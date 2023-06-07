# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


import os

if os.environ.get("UW_PERSON_CLIENT_ENV") == "PROD":
    from compass.clients.person_client import CompassPersonClient
else:
    from compass.clients.mock_person_client import (
        MockedCompassPersonClient as CompassPersonClient)

from uw_person_client.exceptions import (
    PersonNotFoundException, AdviserNotFoundException)
