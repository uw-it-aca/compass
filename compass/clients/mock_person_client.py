# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_person_client.clients.mock_client import MockedUWPersonClient


class MockedCompassPersonClient(MockedUWPersonClient):

    def get_adviser_caseload(self, uwnetid):
        return self.get_persons_by_adviser_netid(uwnetid)
