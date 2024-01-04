# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_person_client import UWPersonClient
from uw_person_client.components import Person, Student, Transcript, Degree
from uw_person_client.exceptions import (
    PersonNotFoundException, AdviserNotFoundException)


class CompassPersonClient(UWPersonClient):

    def get_degrees(self, student_ids):
        degrees = []
        if not len(student_ids):
            return degrees

        sqla_degrees = self.DB.session.query(
            self.DB.Degree.student_id,
            self.DB.Degree.degree_status_desc,
            self.DB.Degree.degree_desc
        ).filter(self.DB.Degree.student_id.in_(student_ids)).order_by(
            self.DB.Degree.degree_date)

        for item in sqla_degrees.all():
            degree = Degree()
            degree.student_id = item[0]
            degree.degree_status_desc = item[1]
            degree.degree_desc = item[2]
            degrees.append(degree)

        return degrees

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
             self.DB.Student.id,
             self.DB.Transcript.scholarship_type,
             self.DB.Transcript.scholarship_desc)\
            .join(self.DB.Person)\
            .join(self.DB.StudentToAdviser)\
            .join(self.DB.Adviser)\
            .join(self.DB.Transcript,
                  self.DB.Student.id == self.DB.Transcript.student_id)\
            .join(self.DB.Term,
                  self.DB.Transcript.tran_term_id == self.DB.Term.id)\
            .order_by(self.DB.Student.id, self.DB.Term.year.desc(),
                      self.DB.Term.quarter.desc())\
            .distinct(self.DB.Student.id)\
            .filter(self.DB.Adviser.id == sqla_adviser.id)

        persons = {}
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
            student_id = item[16]
            latest_transcript = Transcript()
            latest_transcript.scholarship_type = item[17]
            latest_transcript.scholarship_desc = item[18]
            student.transcripts = [latest_transcript]
            student.degrees = []
            person.student = student
            persons[student_id] = person

        for degree in self.get_degrees(persons.keys()):
            persons[degree.student_id].student.degrees.append(degree)

        # sorting by display name, can't get it to work in SQL-Alchemy
        return sorted(persons.values(), key=lambda p: p.display_name)
