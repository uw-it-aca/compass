from uw_person_client.clients.core_client import UWPersonClient
from uw_person_client.components import Person, Student
from uw_person_client.databases.uwpds import UWPDS


class CompassPersonClient(UWPersonClient):

    def __init__(self):
        self.DB = UWPDS()

    def get_adviser_caseload(self, uwnetid):
        sqla_adviser = self.DB.session.query(self.DB.Adviser).join(
            self.DB.Employee).join(self.DB.Person).filter(
            self.DB.Person.uwnetid == uwnetid).one()
        sqla_persons = self.DB.session.query(
             self.DB.Person.display_name,
             self.DB.Person.uwnetid,
             self.DB.Student.gender,
             self.DB.Student.student_number,
             self.DB.Student.class_desc,
             self.DB.Student.registered_in_quarter).join(
            self.DB.Student).join(self.DB.StudentToAdviser).join(
            self.DB.Adviser).filter(self.DB.Adviser.id == sqla_adviser.id)
        persons = []
        for item in sqla_persons.all():
            person = Person()
            person.display_name = item[0]
            person.uwnetid = item[1]
            student = Student()
            student.gender = item[2]
            student.student_numer = item[3]
            student.class_desc = item[4]
            student.registered_in_quarter = item[5]
            person.student = student
            persons.append(item)
        return persons
