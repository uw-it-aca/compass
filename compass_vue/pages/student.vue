// about.vue

<template>
  <layout
    v-if="$route.params.id && person.display_name !== undefined"
    :page-title="person.display_name"
  >
    <template #title>
      <h1 class="visually-hidden">
        {{ person.display_name }}
      </h1>
    </template>
    <template #content>
      <div>
        <div class="row my-4">
          <div class="col">
            <StudentProfile :person="person"></StudentProfile>
          </div>
        </div>

        <div class="row">
          <div class="row p-3">
            <div class="col-8">
              Authorizes Release of Directory Information:
              <span v-if="person.student.directory_release_ind" class="fw-bold"
                >Yes
                <div class="fw-normal text-secondary fs-7">
                  Student has opt out of directory information release, no
                  information may be released about this student. The
                  recommended response is, “I have no information about that
                  individual."
                </div>
              </span>
              <span v-else class="fw-bold">
                No
                <div class="fw-normal text-secondary fs-7">
                  Student has opt out of directory information release, no
                  information may be released about this student. The
                  recommended response is, “I have no information about that
                  individual."
                </div>
              </span>
            </div>
            <div class="col-4">
              <div class="fs-6 text-secondary text-end">
                <i class="bi bi-calendar-week"></i>
                Autumn 2022
              </div>
              <div class="fs-6 text-end">Week 4 of 10</div>
            </div>
          </div>

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
                <axdd-tabs-item :tabs-id="'example'" :panel-id="'history'">
                  History
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
                    <div class="col-xl-12">
                      <StudentAcademics :person="person"></StudentAcademics>
                    </div>
                    <div class="col-xl-9">
                      <StudentSchedule :person="person"></StudentSchedule>
                    </div>
                    <div class="col-xl-3">
                      <StudentAdviser
                        :advisers="person.student.advisers"
                      ></StudentAdviser>
                      <StudentPrograms :person="person"></StudentPrograms>
                    </div>
                  </div>
                </axdd-tabs-panel>
                <axdd-tabs-panel :panel-id="'history'">
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <StudentContact :person="person"></StudentContact>
                    </div>
                    <div class="col-xl-3">
                      <StudentVisits></StudentVisits>
                    </div>
                  </div>
                </axdd-tabs-panel>
                <axdd-tabs-panel :panel-id="'transcript'">
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <StudentTranscript :person="person"></StudentTranscript>
                    </div>
                    <div class="col-xl-3">
                      <StudentTranscriptCredits
                        :person="person"
                      ></StudentTranscriptCredits>
                    </div>
                  </div>
                </axdd-tabs-panel>
              </template>
            </axdd-tabs-display>
          </div>
        </div>
      </div>
    </template>
  </layout>
  <layout v-else :page-title="'Search Student'">
    <template #title>
      <h1 class="visually-hidden">Search Student</h1>
    </template>
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-gray p-3 rounded-3">
            <div class="row">
              <div class="col-xl-4 ms-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <SearchStudent></SearchStudent>
                </div>
              </div>
              <div class="col-4"></div>
              <div class="col-4"></div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import { TabsList, TabsDisplay, TabsItem, TabsPanel } from "axdd-components";

import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

import StudentProfile from "../components/student/profile.vue";
import StudentAcademics from "../components/student/academics.vue";
import StudentTranscript from "../components/student/transcript.vue";
import StudentTranscriptCredits from "../components/student/transcript-credits.vue";
import StudentContact from "../components/student/contact.vue";
import StudentSchedule from "../components/student/schedule.vue";
import StudentAdviser from "../components/student/adviser.vue";
import StudentPrograms from "../components/student/programs.vue";
import StudentVisits from "../components/student/visits.vue";
import TranscriptCredits from "../components/student/transcript-credits.vue";
import SearchStudent from "../components/search-student.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
    StudentProfile,
    StudentAcademics,
    StudentTranscript,
    StudentTranscriptCredits,
    StudentContact,
    StudentSchedule,
    StudentAdviser,
    StudentPrograms,
    StudentVisits,
    TranscriptCredits,
    SearchStudent,
  },
  created: function () {
    this.loadStudent(this.$route.params.id);
  },
  data() {
    return {
      person: {},
    };
  },
  //  computed: {
  //    studentAddress: function () {
  //      let addr = "";
  //      if (this.student.perm_addr_line1)
  //        addr += this.student.perm_addr_line1 + " ";
  //      if (this.student.perm_addr_line2)
  //        addr += this.student.perm_addr_line2 + " ";
  //      if (this.student.perm_addr_city) addr += this.student.perm_addr_city;
  //      if (this.student.perm_addr_state)
  //        addr += ", " + this.student.perm_addr_state;
  //      if (this.student.perm_addr_line1)
  //        addr += " " + this.student.perm_addr_postal_code;
  //      if (addr) return addr;
  //      else return "N/A";
  //    },
  //  },
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
