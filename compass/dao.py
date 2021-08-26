# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import pandas as pd
import pymssql
from compass.models import Term
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from restclients_core.util.retry import retry
from uw_sws.term import get_current_term, get_term_after, \
    get_term_by_year_and_quarter


class SwsDAO():

    @retry(DataFailureException, tries=5, delay=2, backoff=2,
           status_codes=[0, 403, 408, 500])
    def get_sws_terms(self, sis_term_id=None):
        """
        Returns sws term objects for specified sis_term_id onward.

        :param sis_term_id: specify starting sis-term-id to load Term's for.
            For example, if sis_term_id=Spring-2018, then Term Spring-2018 is
            loaded as well as all later Terms in the sws. (defaults to current
            term)
        :type sis_term_id: str
        """
        if sis_term_id is None:
            sws_term = get_current_term()
        else:
            year, quarter = sis_term_id.split("-")
            sws_term = get_term_by_year_and_quarter(int(year), quarter)
        sws_terms = []
        while sws_term:
            sws_terms.append(sws_term)
            try:
                sws_term = get_term_after(sws_term)
            except DataFailureException:
                # next term is not defined
                break
        return sws_terms

    def create_terms(self, sis_term_id=None):
        """
        Creates current term and all future terms

        :param sis_term_id: specify starting sis-term-id to load Term's for.
            For example, if sis_term_id=Spring-2018, then Term Spring-2018 is
            loaded as well as all later Terms in the sws. (defaults to current
            term)
        :type sis_term_id: str
        """
        sws_terms = self.get_sws_terms(sis_term_id=sis_term_id)
        for sws_term in sws_terms:
            term, created = \
                Term.objects.get_or_create_from_sws_term(sws_term)
            if created:
                logging.info(f"Created term {term.sis_term_id}")


class EdwDAO():

    def __init__(self, *args, **kwargs):
        self.configure_pandas()

    def configure_pandas(self):
        """
        Configure global pandas options
        """
        pd.options.mode.use_inf_as_na = True
        pd.options.display.max_rows = 500
        pd.options.display.precision = 3
        pd.options.display.float_format = '{:.3f}'.format

    def get_connection(self, database):
        password = getattr(settings, "EDW_PASSWORD")
        user = getattr(settings, "EDW_USER")
        server = getattr(settings, "EDW_SERVER")
        conn = pymssql.connect(server, user, password, database)
        logging.debug(f"Connected to {server}.{database} with user {user}")
        return conn

    def get_enrolled_students_df(self):
        conn = self.get_connection("EDWPresentation")
        enrolled_df = pd.read_sql(
            """
            SELECT DISTINCT
                enr.SystemKey,
                enr.StudentNumber,
                stu1.uw_netid as UWNetID,
                enr.StudentName,
                enr.StudentNamePreferredFirst,
                enr.StudentNamePreferredMiddle,
                enr.StudentNamePreferredLast,
                enr.BirthDate,
                enr.StudentEmail,
                enr.ExternalEmail,
                enr.LocalPhoneNumber,
                enr.Gender,
                enr.GPA,
                enr.TotalCredits,
                enr.Major1, enr.Major2, enr.Major3,
                enr.Minor1, enr.Minor2, enr.Minor3,
                enr.CampusDesc
            FROM EDWPresentation.sec.EnrolledStudent AS enr
            LEFT JOIN UWSDBDataStore.sec.student_1 AS stu1 ON enr.SystemKey = stu1.system_key
            WHERE AcademicYrQtr = '20212'
            """,  # noqa
            conn
        )
        return enrolled_df