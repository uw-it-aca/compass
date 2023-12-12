<template>
  <layout :page-title="'Student Search'">
    <template #title>
      <h1 class="visually-hidden">
        <template v-if="$route.params.id && person.display_name !== undefined">
          {{ person.display_name }}
        </template>
        <template v-else>Student Search</template>
      </h1>
    </template>
    <template #content>
      <div v-show="!$route.params.id || isError" class="row my-4 small">
        <div class="col">
          <div class="bg-light p-3 rounded-3">
            <div class="row">
              <div class="col-xl-4 ms-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <SearchStudent :error="isError"></SearchStudent>
                </div>
              </div>
              <div class="col-4"></div>
              <div class="col-4"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="isLoading">
        <div class="row my-4">
          <div class="col">
            <StudentProfileLoading></StudentProfileLoading>
          </div>
        </div>
      </div>
      <div v-else-if="$route.params.id && person.display_name !== undefined">
        <div class="row my-4">
          <div class="col">
            <StudentProfile :person="person"></StudentProfile>
          </div>
        </div>

        <div class="row my-5">
          <div class="col-12">
            <div>
              Student Authorizes Release of Directory Information:
              <span
                class="small badge rounded-pill text-bg-secondary border-0 px-2 py-1 mb-0 me-1"
              >
                <template v-if="person.student.directory_release_ind"
                  >Yes</template
                >
                <template v-else>No</template>
              </span>
            </div>
            <div
              v-if="!person.student.directory_release_ind"
              class="fw-normal text-secondary small"
            >
              This student has opted out and blocked the release of their
              directory information. No information may be released about this
              student. A recommended response when asked about this student is,
              "I have no information about that individual."
            </div>
            <div>
              <a
                href="https://registrar.washington.edu/staffandfaculty/ferpa/"
                class="small"
                target="_blank"
              >
                Learn More</a
              >
            </div>
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
                <axdd-tabs-item
                  :tabs-id="'example'"
                  :panel-id="'contact-visit'"
                >
                  Contacts &amp; Visits
                </axdd-tabs-item>
                <axdd-tabs-item
                  :tabs-id="'example'"
                  :panel-id="'academic-history'"
                >
                  Academic History
                </axdd-tabs-item>

                <!-- MARK: only show administrative tab to managers -->
                <axdd-tabs-item
                  v-show="userRoles.includes(Role.Manager)"
                  :tabs-id="'example'"
                  :panel-id="'admin'"
                >
                  Administrative
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
                      <StudentHolds :person="person"></StudentHolds>
                      <StudentAdviser
                        :advisers="person.student.advisers"
                      ></StudentAdviser>
                    </div>
                  </div>
                </axdd-tabs-panel>
                <axdd-tabs-panel :panel-id="'contact-visit'">
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <StudentContact :person="person"></StudentContact>
                    </div>
                    <div class="col-xl-3">
                      <StudentVisits :person="person"></StudentVisits>
                    </div>
                  </div>
                </axdd-tabs-panel>
                <axdd-tabs-panel :panel-id="'academic-history'">
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

                <!-- MARK: only show administrative panel to managers -->
                <axdd-tabs-panel
                  v-show="userRoles.includes(Role.Manager)"
                  :panel-id="'admin'"
                >
                  <div class="row mt-4">
                    <div class="col-xl-9">
                      <AffiliationAddEdit :person="person"></AffiliationAddEdit>
                    </div>
                    <div class="col-xl-3">&nbsp;</div>
                  </div>
                </axdd-tabs-panel>
              </template>
            </axdd-tabs-display>
          </div>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import { Role } from "@/utils/roles.js";
import Layout from "@/layout.vue";
import dataMixin from "@/mixins/data_mixin.js";
import StudentProfile from "@/components/student/profile.vue";
import StudentProfileLoading from "@/components/student/profile-loading.vue";
import StudentAcademics from "@/components/student/academics.vue";
import StudentTranscript from "@/components/student/transcript.vue";
import StudentTranscriptCredits from "@/components/student/transcript-credits.vue";
import StudentContact from "@/components/student/contact.vue";
import StudentSchedule from "@/components/student/schedule.vue";
import StudentHolds from "@/components/student/holds.vue";
import StudentAdviser from "@/components/student/adviser.vue";
import StudentVisits from "@/components/student/visits.vue";
import SearchStudent from "@/components/search-student.vue";
import AffiliationAddEdit from "@/components/student/administrative/affiliation.vue";

export default {
  mixins: [dataMixin],
  inject: ["mq"],
  components: {
    layout: Layout,
    StudentProfile,
    StudentProfileLoading,
    StudentAcademics,
    StudentTranscript,
    StudentTranscriptCredits,
    StudentContact,
    StudentSchedule,
    StudentHolds,
    StudentAdviser,
    StudentVisits,
    SearchStudent,
    AffiliationAddEdit,
  },
  created: function () {
    this.loadAccessGroups();
    if (this.$route.params.id) {
      this.isLoading = true;
      //setTimeout(() => {
      this.loadStudent(this.$route.params.id);
      //}, 3000);
    }
  },
  data() {
    return {
      person: {},
      isLoading: false,
      isError: false,
      accessGroups: [],
      userRoles: document.body.getAttribute("data-user-role").split(","),
      Role: Role,
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
      this.getStudentDetail(studentNetID)
        .then((response) => {
          if (response.data) {
            this.person = response.data;
            this.isLoading = false;
            this.isError = false;

            // programatically update page title with student name
            document.title = this.person.display_name + " - Compass";
          }
        })
        .catch((error) => {
          this.isLoading = false;
          this.isError = true;
          console.log("error occured: " + error);
        });
    },
    loadAccessGroups: function () {
      this.getAccessGroups().then((response) => {
        if (response.data) {
          this.accessGroups = response.data;
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
