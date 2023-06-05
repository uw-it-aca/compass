# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.components import Person, Student, Transcript
from uw_person_client.databases.uwpds import UWPDS
from uw_person_client.exceptions import AdviserNotFoundException


class CompassPersonClient(UWPersonClient):

    def __init__(self):
        self.DB = UWPDS()

    def get_adviser_caseload(self, uwnetid):
        sqla_adviser = self.DB.session.query(self.DB.Adviser).join(
            self.DB.Employee).join(self.DB.Person).filter(
            self.DB.Person.uwnetid == uwnetid).one_or_none()
        if not sqla_adviser:
            raise AdviserNotFoundException()
        sqla_persons = self.DB.session.query(
             self.DB.Person.display_name,
             self.DB.Person.uwnetid,
             self.DB.Person.uwregid,
             self.DB.Person.pronouns,
             self.DB.Student.student_number,
             self.DB.Student.gender,
             self.DB.Student.student_number,
             self.DB.Student.class_desc,
             self.DB.Student.registered_in_quarter,
             self.DB.Student.registration_hold_ind,
             self.DB.Student.campus_desc,
             self.DB.Student.special_program_code,
             self.DB.Student.special_program_desc,
             self.DB.Student.enroll_status_code,
             self.DB.Student.enroll_status_request_code,
             self.DB.Student.enroll_status_desc,
             self.DB.Transcript.scholarship_type,
             self.DB.Transcript.scholarship_desc,)\
            .join(self.DB.Person)\
            .join(self.DB.StudentToAdviser)\
            .join(self.DB.Adviser) \
            .join(self.DB.Transcript,
                  self.DB.Student.id == self.DB.Transcript.student_id) \
            .join(self.DB.Term,
                  self.DB.Transcript.tran_term_id == self.DB.Term.id) \
            .order_by(self.DB.Student.id, self.DB.Term.year.desc(),
                      self.DB.Term.quarter.desc()) \
            .distinct(self.DB.Student.id) \
            .filter(self.DB.Adviser.id == sqla_adviser.id)
        persons = []
        for item in sqla_persons.all():
            person = Person()
            person.display_name = item[0]
            person.uwnetid = item[1]
            person.uwregid = item[2]
            person.pronouns = item[3]
            student = Student()
            student.student_number = item[4]
            student.gender = item[5]
            student.student_numer = item[6]
            student.class_desc = item[7]
            student.registered_in_quarter = item[8]
            student.registration_hold_ind = item[9]
            student.campus_desc = item[10]
            student.special_program_code = item[11]
            student.special_program_desc = item[12]
            student.enroll_status_code = item[13]
            student.enroll_status_request_code = item[14]
            student.enroll_status_desc = item[15]
            latest_transcript = Transcript()
            latest_transcript.scholarship_type = item[16]
            latest_transcript.scholarship_desc = item[17]
            student.transcripts = [latest_transcript]
            person.student = student
            persons.append(person)
        # sorting by display name, can't get it to work in SQL-Alchemy
        persons.sort(key=lambda x: x.display_name)

        return persons
