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
          <div class="col">
            <axdd-tabs-list :tabs-id="'example'">
              <template #items>
                <axdd-tabs-item
                  :tabs-id="'example'"
                  :panel-id="'overview'"
                  :active-tab="true"
                >
                  Overview
                </axdd-tabs-item>
                <axdd-tabs-item :tabs-id="'example'" :panel-id="'advising'">
                  Advising
                </axdd-tabs-item>
                <axdd-tabs-item :tabs-id="'example'" :panel-id="'transcript'">
                  Unofficial Transcript
                </axdd-tabs-item>
              </template>
            </axdd-tabs-list>

            <axdd-tabs-display :tabs-id="'example'">
              <template #panels>
                <axdd-tabs-panel :panel-id="'overview'" :active-panel="true">
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <StudentAcademics :person="person"></StudentAcademics>
                      <StudentSchedule :person="person"></StudentSchedule>
                    </div>
                    <div class="col-xl-3">
                      <StudentAddress :person="person"></StudentAddress>
                      <StudentEmergencyContact :person="person"></StudentEmergencyContact>
                    </div>
                  </div>
                </axdd-tabs-panel>
                <axdd-tabs-panel :panel-id="'advising'">
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <StudentContact :person="person"></StudentContact>
                      <StudentVisits></StudentVisits>
                    </div>
                    <div class="col-xl-3">
                      <StudentAdviser
                        :advisers="person.student.advisers"
                      ></StudentAdviser>
                      <StudentPrograms :person="person"></StudentPrograms>
                    </div>
                  </div>
                </axdd-tabs-panel>
                <axdd-tabs-panel :panel-id="'transcript'">
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <StudentTranscript :person="person"></StudentTranscript>
                    </div>
                    <div class="col-xl-3">
                      <StudentTranscriptCredits></StudentTranscriptCredits>
                    </div>
                  </div>
                </axdd-tabs-panel>
              </template>
            </axdd-tabs-display>
          </div>
        </div>
      </div>
      <div v-else>No student</div>
    </template>
  </layout>
</template>

<script>
import { TabsList, TabsDisplay, TabsItem, TabsPanel } from "axdd-components";

import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

import StudentProfile from "../components/student/profile.vue";
import StudentAddress from "../components/student/address.vue";
import StudentEmergencyContact from "../components/student/emergency.vue";
import StudentAcademics from "../components/student/academics.vue";
import StudentTranscript from "../components/student/transcript.vue";
import StudentTranscriptCredits from "../components/student/transcript-credits.vue";
import StudentContact from "../components/student/contact.vue";
import StudentSchedule from "../components/student/schedule.vue";
import StudentAdviser from "../components/student/adviser.vue";
import StudentPrograms from "../components/student/programs.vue";
import StudentVisits from "../components/student/visits.vue";
import TranscriptCredits from "../components/student/transcript-credits.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
    StudentProfile,
    StudentAddress,
    StudentEmergencyContact,
    StudentAcademics,
    StudentTranscript,
    StudentTranscriptCredits,
    StudentContact,
    StudentSchedule,
    StudentAdviser,
    StudentPrograms,
    StudentVisits,
    TranscriptCredits
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
    loadStudent: function (studentNetID) {
      this.getStudentDetail(studentNetID).then((response) => {
        if (response.data) {
          this.person = response.data;
        }
      });
    },
  },
};
</script>

<style lang="scss">
.table {
  tbody tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
