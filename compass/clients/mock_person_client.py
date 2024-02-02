# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_person_client.clients.mock_client import MockedUWPersonClient


class MockedCompassPersonClient(MockedUWPersonClient):

    def get_adviser_caseload(self, uwnetid):
        return self.get_persons_by_adviser_netid(uwnetid)

    def get_appuser_by_uwnetid(self, uwnetid):
        return self.get_person_by_uwnetid(
            uwnetid,
            include_employee=False,
            include_student=False,
            include_student_transcripts=False,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_majors=False,
            include_student_pending_majors=False,
            include_student_holds=False,
            include_student_degrees=False)
