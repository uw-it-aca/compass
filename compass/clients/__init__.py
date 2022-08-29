# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os

if os.environ.get("AXDD_PERSON_CLIENT_ENV") == "PROD":
    from compass.cients.person_client import CompassPersonClient
else:
    from compass.clients.mock_person_client import \
        MockedCompassPersonClient as CompassPersonClient  # noqa
