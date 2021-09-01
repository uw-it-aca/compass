# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from compass.dao import EdwDAO
from compass.views.api import RESTDispatch


class EnrolledStudentsListView(RESTDispatch):
    '''
    API endpoint returning a list of users from the EDW

    /api/internal/edw/enrolled-students/

    HTTP POST accepts the following dictionary parameters:
    * filters: dictionary of request filters
    '''
    def post(self, request, *args, **kwargs):
        edw_dao = EdwDAO()
        df = edw_dao.get_enrolled_students_df()
        return self.json_response(content=df.to_dict('records'))
