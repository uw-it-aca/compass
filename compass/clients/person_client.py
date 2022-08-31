# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.components import Person, Student
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
             self.DB.Student.student_number,
             self.DB.Student.gender,
             self.DB.Student.student_number,
             self.DB.Student.class_desc,
             self.DB.Student.registered_in_quarter,
             self.DB.Student.campus_desc,
             self.DB.Student.enroll_status_code).join(
            self.DB.Student).join(self.DB.StudentToAdviser).join(
            self.DB.Adviser).filter(
                self.DB.Adviser.id == sqla_adviser.id).order_by(
            self.DB.Person.display_name)
        persons = []
        for item in sqla_persons.all():
            person = Person()
            person.display_name = item[0]
            person.uwnetid = item[1]
            person.uwregid = item[2]
            student = Student()
            student.student_number = item[3]
            student.gender = item[4]
            student.student_numer = item[5]
            student.class_desc = item[6]
            student.registered_in_quarter = item[7]
            student.campus_desc = item[8]
            student.enroll_status_code = item[9]
            person.student = student
            persons.append(person)
        return persons
