# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from compass.models import Term, Student, Major
from restclients_core.exceptions import DataFailureException
from restclients_core.util.retry import retry
from uw_sws.term import get_current_term, get_term_after, \
    get_term_by_year_and_quarter
from edw_clients.compass.dao import EDWCompassDAO


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


class EDWClientDAO():

    def load_enrolled_students(self, sis_term_id):
        edw_client = EDWCompassDAO()
        enrolled_students_df = edw_client.get_enrolled_students_df(sis_term_id)
        for _, row in enrolled_students_df.iterrows():
            stunum = row["StudentNumber"]
            student, _ = Student.objects.get_or_create(student_number=stunum)
            student.student_number = stunum
            student.uw_net_id = row["UWNetID"]
            student.student_name = row["StudentName"]
            student.birthdate = row["BirthDate"]
            student.student_email = row["StudentEmail"]
            student.external_email = row["ExternalEmail"]
            student.local_phone_number = row["LocalPhoneNumber"]
            student.gender = row["Gender"]
            student.gpa = row["GPA"]
            student.total_credits = row["TotalCredits"]
            student.class_desc = row["ClassDesc"]
            student.enrollment_status = row["EnrollStatusCode"]
            major_abbr = row["major_abbr"]
            major, _ = Major.objects.get_or_create(major_abbr_code=major_abbr)
            major.major_abbr_code = row["major_abbr"]
            major.major_name = row["major_name"]
            major.major_full_name = row["major_full_nm"]
            major.major_short_name = row["major_short_nm"]
            major.save()
            student.major.add(major)
            student.save()
