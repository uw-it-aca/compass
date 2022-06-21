// about.vue

<template>
  <layout
    v-if="person.display_name !== undefined"
    :page-title="person.display_name"
  >
    <template #title>
      <h1 v-if="$route.params.id" class="visually-hidden">
        {{ person.display_name }}
      </h1>
      <h1 v-else>Student</h1>
    </template>
    <template #content>
      <div v-if="$route.params.id">
        <div class="row my-4">
          <div class="col">
            <StudentProfile :person="person"></StudentProfile>
          </div>
        </div>

        <div class="row">
          <div class="col-xl-9">
             <StudentAcademics :person="person"></StudentAcademics>
            <StudentContact
              :person="person"
              :contacts="contacts"
            ></StudentContact>
            <StudentSchedule :schedules="schedules"></StudentSchedule>
            <StudentVisits></StudentVisits>
          </div>
          <div class="col-xl-3">
            <StudentAdviser
              :advisers="person.student.advisers"
            ></StudentAdviser>
            <StudentPrograms :person="person"></StudentPrograms>
          </div>
        </div>
      </div>
      <div v-else>No student</div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";


import StudentProfile from "../components/student/profile.vue";
import StudentAcademics from "../components/student/academics.vue";
import StudentContact from "../components/student/contact.vue";
import StudentSchedule from "../components/student/schedule.vue";
import StudentAdviser from "../components/student/adviser.vue";
import StudentPrograms from "../components/student/programs.vue";
import StudentVisits from "../components/student/visits.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    StudentProfile,
    StudentAcademics,
    StudentContact,
    StudentSchedule,
    StudentAdviser,
    StudentPrograms,
    StudentVisits,
  },
  created: function () {
    this.loadStudent(this.$route.params.id);
  },
  data() {
    return {
      person: {},
      contacts: {},
      schedules: {},
      programs: {},
      specialPrograms: {},
    };
  },
  computed: {
    studentAddress: function () {
      let addr = "";
      if (this.student.perm_addr_line1)
        addr += this.student.perm_addr_line1 + " ";
      if (this.student.perm_addr_line2)
        addr += this.student.perm_addr_line2 + " ";
      if (this.student.perm_addr_city) addr += this.student.perm_addr_city;
      if (this.student.perm_addr_state)
        addr += ", " + this.student.perm_addr_state;
      if (this.student.perm_addr_line1)
        addr += " " + this.student.perm_addr_postal_code;
      if (addr) return addr;
      else return "N/A";
    },
  },
  methods: {
    loadStudent: function (studentNetID) {
      let _this = this;
      this.getStudentDetail(studentNetID).then((response) => {
        if (response.data) {
          _this.person = response.data;
          this.loadStudentContacts(_this.person.student.system_key);
          this.loadStudentSchedules(_this.person.uwregid);
          this.loadStudentPrograms(_this.person.student.system_key);
          this.loadStudentSpecialPrograms(_this.person.student.system_key);
        }
      });
    },
    loadStudentContacts: function (studentSystemKey) {
      let _this = this;
      this.getStudentContacts(studentSystemKey).then((response) => {
        if (response.data) {
          _this.contacts = response.data;
        }
      });
    },
    loadStudentPrograms: function (studentSystemKey) {
      let _this = this;
      this.getStudentPrograms(studentSystemKey).then((response) => {
        if (response.data) {
          _this.programs = response.data;
        }
      });
    },
    loadStudentSpecialPrograms: function (studentSystemKey) {
      let _this = this;
      this.getStudentSpecialPrograms(studentSystemKey).then((response) => {
        if (response.data) {
          _this.specialPrograms = response.data;
        }
      });
    },
    loadStudentSchedules: function (studentRegID) {
      let _this = this;
      this.getStudentSchedules(studentRegID).then((response) => {
        if (response.data) {
          _this.schedules = response.data;
        }
      });
    },
  },
};
</script>

<style lang="scss">
.table {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
