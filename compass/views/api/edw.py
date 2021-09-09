# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from compass.models import Term
from compass.views.api import RESTDispatch
from edw_clients.compass.dao import CompassDAO


class EnrolledStudentsListView(RESTDispatch):
    '''
    API endpoint returning a list of users from the EDW

    /api/internal/edw/enrolled-students/

    HTTP POST accepts the following dictionary parameters:
    * filters: dictionary of request filters
    '''
    def post(self, request, *args, **kwargs):
        filters = json.loads(request.body.decode('utf-8'))
        compass_dao = CompassDAO()
        curr_term, _ = Term.objects.get_or_create_term_from_sis_term_id()
        enrolled_students_df = compass_dao.get_enrolled_students_df(
            curr_term.sis_term_id, filters=filters)
        return self.json_response(
            content=enrolled_students_df.to_dict('records'))


class EnrolledStudentsCount(RESTDispatch):
    '''
    API endpoint returning a count of enrolled users from the EDW

    /api/internal/edw/enrolled-students-count/
    '''
    def post(self, request, *args, **kwargs):
        compass_dao = CompassDAO()
        curr_term, _ = Term.objects.get_or_create_term_from_sis_term_id()
        enrolled_students_count = compass_dao.get_number_enrolled_students(
            curr_term.sis_term_id)
        return self.json_response(
            content={'enrolled_students_count': enrolled_students_count})
