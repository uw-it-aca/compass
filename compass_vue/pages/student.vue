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
            <StudentContact></StudentContact>
            <StudentSchedule></StudentSchedule>
            <StudentHistory :person="person"></StudentHistory>
          </div>
          <div class="col-xl-3">
            <StudentAdviser
              :advisers="person.student.advisers"
            ></StudentAdviser>
            <StudentPrograms :person="person"></StudentPrograms>
            <StudentAcademics :person="person"></StudentAcademics>
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
import StudentContact from "../components/student/contact.vue";
import StudentSchedule from "../components/student/schedule.vue";
import StudentHistory from "../components/student/history.vue";
import StudentAdviser from "../components/student/adviser.vue";
import StudentPrograms from "../components/student/programs.vue";
import StudentAcademics from "../components/student/academics.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    StudentProfile,
    StudentContact,
    StudentSchedule,
    StudentHistory,
    StudentAdviser,
    StudentPrograms,
    StudentAcademics,
  },
  created: function () {
    this.loadStudent(this.$route.params.id);
  },
  data() {
    return {
      person: {},
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
    loadStudent: function (studentNumber) {
      let _this = this;
      this.getStudentDetail(studentNumber).then((response) => {
        if (response.data) {
          _this.person = response.data;
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
