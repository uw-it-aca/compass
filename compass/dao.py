# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
import pandas as pd
import random
import string
from compass.models import Term, Student, Major, SpecialProgram
from csv import DictReader
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db import transaction
from django.urls import reverse
from restclients_core.exceptions import DataFailureException
from restclients_core.util.retry import retry
from uw_canvas import Canvas
from uw_canvas.reports import Reports
from uw_canvas.terms import Terms
from uw_sws.term import get_current_term, get_term_after, \
    get_term_by_year_and_quarter
from uw_pws import PWS
from urllib.parse import urlparse, urlunparse
from edw_clients.compass.dao import EDWCompassDAO

class BaseDAO():
    """
    Data Access Object for common data access methods
    """

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


class CanvasDAO(BaseDAO):
    """
    Data Access Object for accessing canvas data
    """

    def __init__(self):
        self.canvas = Canvas()
        self.reports = Reports()
        self.terms = Terms()
        super().__init__()

    def configure_pandas(self):
        """
        Configure global pandas options
        """
        pd.options.mode.use_inf_as_na = True
        pd.options.display.max_rows = 500
        pd.options.display.precision = 3
        pd.options.display.float_format = '{:.3f}'.format

    def download_user_provisioning_report(self, sis_term_id=None):
        """
        Download canvas sis user provisioning report

        :param sis_term_id: sis term id to load users report for
        :type sis_term_id: str
        """
        term, _ = Term.objects.get_or_create_term_from_sis_term_id(
            sis_term_id=sis_term_id)
        # get canvas term using sis-term-id
        canvas_term = self.terms.get_term_by_sis_id(term.sis_term_id)
        # get users provisioning repmiort for canvas term
        user_report = self.reports.create_user_provisioning_report(
                    getattr(settings, "ACADEMIC_CANVAS_ACCOUNT_ID", "84378"),
                    term_id=canvas_term.term_id,
                    params={"created_by_sis": True})
        logging.info(f"Downloading user provisioning report: "
                     f"term={sis_term_id}")
        sis_data = self.reports.get_report_data(user_report)
        self.reports.delete_report(user_report)
        return sis_data

    def update_students_from_canvas(self, sis_term_id):
        logging.info("Adding canvas context to students")
        # get provising data and load courses
        cd = CanvasDAO()
        sis_data = cd.download_user_provisioning_report(
            sis_term_id=sis_term_id)

        logging.info(f"Parsing Canvas user provisioning report "
                     f"containing {len(sis_data)} rows.")

        pws = PWS()
        student_count = 0

        with transaction.atomic():
            for row in DictReader(sis_data):
                if not len(row):
                    continue
                created_by_sis = row['created_by_sis']
                status = row['status']
                sis_user_id = row['user_id']
                canvas_user_id = int(row['canvas_user_id'])
                if created_by_sis == "true" and status == "active" and \
                        pws.valid_uwregid(sis_user_id):
                    uw_net_id = str(row['login_id']).strip()
                    try:
                        student = Student.objects.get(
                            uw_net_id=uw_net_id)
                    except Student.DoesNotExist:
                        continue
                    student.uw_reg_id = sis_user_id
                    student.canvas_user_id = canvas_user_id
                    student.save()
                    student_count += 1
        return student_count


class PwsDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def cache_key(self, key):
        return 'idphoto-key-{}'.format(key)

    def get_photo(self, photo_key):
        data = cache.get(self.cache_key(photo_key))
        cache.delete(self.cache_key(photo_key))

        if data is None:
            raise ObjectDoesNotExist()

        return PWS().get_idcard_photo(
            data.get('reg_id'), size=data.get('image_size'))

    def get_photo_url(self, reg_id, image_size="small"):
        """ Returns a url for the IDPhoto
        """
        if PWS().valid_uwregid(reg_id):
            photo_key = ''.join(random.SystemRandom().choice(
                string.ascii_lowercase + string.digits) for _ in range(16))

            data = {'reg_id': reg_id, 'image_size': image_size}
            expires = getattr(settings, 'IDCARD_TOKEN_EXPIRES', 60 * 60)
            cache.set(self.cache_key(photo_key), data, timeout=expires)
            return reverse('photo', kwargs={'photo_key': photo_key})

    def get_avatar_url(self, url, image_size):
        """ Modifies the passed url based on image_size
        """
        url_parts = urlparse(url)
        if 'gravatar.com' in url_parts.netloc:
            new_parts = url_parts._replace(
                query='s={}&d=mm'.format(image_size))
            return urlunparse(new_parts)
        return url


class SwsDAO(BaseDAO):

    def __init__(self):
        super().__init__()

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


class EDWClientDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def load_students_from_edw(self, sis_term_id):
        logging.info("Loading initial student info from the EDW.")
        edw_client = EDWCompassDAO()
        students_df = edw_client.get_enrolled_students_df(sis_term_id)
        logging.info("Downloaded {} records from the EDW.".format(
            students_df[students_df.columns[0]].count()
        ))
        for _, row in students_df.iterrows():
            uw_net_id = row["UWNetID"]
            student, _ = Student.objects.get_or_create(uw_net_id=uw_net_id)
            student.student_number = row["StudentNumber"]
            student.student_name = row["StudentName"]
            student.student_preferred_first_name = \
                row["StudentNamePreferredFirst"]
            student.student_preferred_middle_name = \
                row["StudentNamePreferredMiddle"]
            student.student_preferred_last_name = \
                row["StudentNamePreferredLast"]
            student.birthdate = row["BirthDate"]
            student.student_email = row["StudentEmail"]
            student.external_email = row["ExternalEmail"]
            student.local_phone_number = row["LocalPhoneNumber"]
            student.gender = row["Gender"]
            student.gpa = row["GPA"]
            student.total_credits = row["TotalCredits"]
            student.total_uw_credits = row["TotalUWCredits"]
            student.campus_code = row["CampusCode"]
            student.campus_desc = row["CampusDesc"]
            student.class_code = row["ClassCode"]
            student.class_desc = row["ClassDesc"]
            student.enrollment_status_code = row["EnrollStatusCode"]
            student.exemption_code = row["ExemptionCode"]
            student.exemption_desc = row["ExemptionDesc"]
            special_program, _ = SpecialProgram.objects.get_or_create(
                special_program_code=row["SpecialProgramCode"],
                special_program_desc=row["SpecialProgramDesc"]
            )
            student.special_program.add(special_program)
            student.honors_program_code = row["HonorsProgramCode"]
            student.honors_program_ind = row["HonorsProgramInd"]
            student.resident_code = row["ResidentCode"]
            student.resident_desc = row["ResidentDesc"]
            student.perm_addr_line1 = row["PermAddrLine1"]
            student.perm_addr_line2 = row["PermAddrLine2"]
            student.perm_addr_city = row["PermAddrCity"]
            student.perm_addr_state = row["PermAddrState"]
            student.perm_addr_5digit_zip = row["PermAddr5DigitZip"]
            student.perm_addr_4digit_zip = row["PermAddr4DigitZip"]
            student.perm_addr_country = row["PermAddrCountry"]
            student.perm_addr_postal_code = row["PermAddrPostalCode"]
            student.registered_in_quarter = \
                (True if row["RegisteredInQuarter"] == 'Y' else False)
            major_abbr = row["major_abbr"]
            major, _ = Major.objects.get_or_create(major_abbr_code=major_abbr)
            major.major_abbr_code = row["major_abbr"]
            major.major_name = row["major_name"]
            major.major_full_name = row["major_full_nm"]
            major.major_short_name = row["major_short_nm"]
            major.save()
            student.major.add(major)
            student.save()
        logging.info("Saved {} records into the Compass DB.".format(
            students_df[students_df.columns[0]].count()
        ))


class TaskDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def create_or_update_students(self, sis_term_id):
        """
        Create and or updates students table for a term

        :param sis_term_id: sis term id to load users for. (default is
            the current term)
        :type sis_term_id: str
        """
        EDWClientDAO().load_students_from_edw(sis_term_id)
        CanvasDAO().update_students_from_canvas(sis_term_id)
