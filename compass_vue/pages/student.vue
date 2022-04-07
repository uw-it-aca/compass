// about.vue

<template>
  <axdd-layout v-if="student.student_name !== undefined" :page-title="student.student_name">
    <template #title>
      <h1 v-if="$route.params.id" class="visually-hidden">{{ student.student_name }}</h1>
      <h1 v-else>Student</h1>
    </template>
    <template #content>
      <div v-if="$route.params.id">
        <div class="row my-4">
          <div class="col">
            <div class="bg-gray p-4 rounded-3">
              <div class="row">
                <div class="col-lg-6 pe-4 d-flex small">
                  <div>
                    <div
                      :class="priorityRing"
                      class="rounded-circle border border-4"
                      style="width: 140px"
                    >
                      <img
                        v-if="student.gender === 'F'"
                        :src="'https://randomuser.me/api/portraits/women/' + student.id + '.jpg'"
                        class="img-fluid rounded-circle border border-light border-3"
                      />
                      <img
                        v-else
                        :src="'https://randomuser.me/api/portraits/men/' + student.id + '.jpg'"
                        class="img-fluid rounded-circle border border-light border-3"
                      />
                    </div>
                    <div class="text-center mb-4">
                      <span class="fw-bold">Priority {{ student.retention.priority }}</span>
                    </div>
                  </div>
                  <div class="flex-fill ps-4 mb-4">
                    <div class="h3 text-dark axdd-font-encode-sans">
                      {{ student.student_preferred_last_name }},
                      {{ student.student_preferred_first_name }}
                    </div>
                    <div class="h5">
                      {{ $route.params.id }}, <small>{{ student.uw_net_id }}</small>
                    </div>
                    <p>
                      <span class="badge rounded-pill border border-muted text-dark me-1">{{
                        student.gender
                      }}</span>
                      <span
                        v-if="student.gender === 'F'"
                        class="badge rounded-pill border border-muted text-dark"
                        >she/her</span
                      >
                      <span v-else class="badge rounded-pill border border-muted text-dark"
                        >he/him</span
                      >
                    </p>
                    <div>
                      <i class="bi bi-trophy-fill text-purple"></i> Sport: Track &amp; Field
                    </div>
                  </div>
                </div>
                <div class="col-6 col-lg-3 px-4 small">
                  <ul class="list-unstyled m-0">
                    <li>
                      Preferred name: {{ student.student_preferred_first_name }}
                      {{ student.student_preferred_middle_name }}
                      {{ student.student_preferred_last_name }}
                    </li>
                    <li>Ethnicity:</li>
                    <li>Citizenship: {{ student.resident_desc }}</li>
                    <li>DOB: 7/23/2001</li>
                  </ul>
                </div>
                <div class="col-6 col-lg-3 ps-4 small">
                  <ul class="list-unstyled m-0">
                    <li>UW Email: {{ student.student_email }}</li>
                    <li>Personal email: {{ student.personal_email }}</li>
                    <li>Local Phone: {{ student.local_phone_number }}</li>
                    <li>Perm Address: {{ studentAddress }}</li>
                    <li>
                      Local Address: 1234
                      <a href="#" class="small" role="button">Edit address (ALL)</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-xl-9">
            <StudentContact></StudentContact>
            <StudentSchedule></StudentSchedule>
            <StudentHistory></StudentHistory>
          </div>
          <div class="col-xl-3">
            <StudentAdviser></StudentAdviser>
            <StudentPrograms :student="student"></StudentPrograms>
            <StudentRetention :student="student"></StudentRetention>
            <StudentAcademics :student="student"></StudentAcademics>
            <StudentMajors :student="student"></StudentMajors>
          </div>
        </div>

      </div>
      <div v-else>No student</div>
    </template>
  </axdd-layout>
</template>

<script>
import { Card } from 'axdd-components';

import Tabs from '../_components/tabs/tabs.vue';
import TabItem from '../_components/tabs/item.vue';
import TabPanel from '../_components/tabs/panel.vue';

import Layout from '../layout.vue';
import dataMixin from '../mixins/data_mixin.js';

import StudentContact from '../components/student/contact.vue'
import StudentSchedule from '../components/student/schedule.vue';
import StudentHistory from '../components/student/history.vue';
import StudentAdviser from '../components/student/adviser.vue';
import StudentPrograms from '../components/student/programs.vue';
import StudentRetention from '../components/student/retention.vue';
import StudentAcademics from '../components/student/academics.vue';
import StudentMajors from '../components/student/majors.vue';

export default {
  mixins: [dataMixin],
  components: {
    "axdd-layout": Layout,
    "axdd-card": Card,
    "axdd-tabs": Tabs,
    "axdd-tab-item": TabItem,
    "axdd-tab-panel": TabPanel,
    StudentContact,
    StudentSchedule,
    StudentHistory,
    StudentAdviser,
    StudentPrograms,
    StudentRetention,
    StudentAcademics,
    StudentMajors
},
  created: function () {
    this.loadstudent(this.$route.params.id);
  },
  data() {
    return {
      student: {},
    };
  },
  computed: {
    studentAddress: function () {
      let addr = '';
      if (this.student.perm_addr_line1) addr += this.student.perm_addr_line1 + ' ';
      if (this.student.perm_addr_line2) addr += this.student.perm_addr_line2 + ' ';
      if (this.student.perm_addr_city) addr += this.student.perm_addr_city;
      if (this.student.perm_addr_state) addr += ', ' + this.student.perm_addr_state;
      if (this.student.perm_addr_line1) addr += ' ' + this.student.perm_addr_postal_code;
      if (addr) return addr;
      else return 'N/A';
    },
    priorityRing: function () {
      // mocked display
      if (this.student.retention.priority === '-3.4') {
        return 'border-danger';
      } else if (this.student.retention.priority === '2.2') {
        return 'border-warning';
      } else {
        return '';
      }
    },
  },
  methods: {
    loadstudent: function (studentNumber) {
      let _this = this;
      this.getStudentDetail(studentNumber).then((response) => {
        if (response.data) {
          _this.student = response.data[0];
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
