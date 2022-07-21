<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-gray p-3 rounded-3">
            <div class="row">
              <div class="col-4">
                <div class="fw-bold lh-lg">Filter by adviser:</div>
                <div>
                  <search-adviser></search-adviser>
                </div>
              </div>
              <div class="col-4 border-start ms-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <search-student></search-student>
                </div>
              </div>
              <div class="col-4 d-flex border-start">
                <div class="flex-fill me-3">
                  <div class="fw-bold lh-lg">Class Standing:</div>
                  <select
                    class="form-select form-select-sm"
                    aria-label=".form-select-sm example"
                  >
                    <option selected>All</option>
                    <option value="1">Freshman</option>
                    <option value="2">Sophomore</option>
                    <option value="3">Junior</option>
                    <option value="4">Senior</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2">My Caseload</axdd-card-heading>
            </template>
            <template #body>
              <table-loading v-if="isLoading"></table-loading>
              <div v-else class="table-responsive">
                <table v-if="persons" class="table mb-0">
                  <thead class="small">
                    <tr>
                      <th scope="col" class="ps-0">Student</th>
                      <th scope="col">Class</th>
                      <th scope="col">Campus</th>
                      <th scope="col" class="text-nowrap">Enrollment Status</th>
                      <th scope="col">Adviser</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="person in persons"
                      :key="person.uwnetid"
                      class="bg-light-hover"
                    >
                      <td>
                        <profile-mini :person="person"></profile-mini>
                      </td>
                      <td>{{ person.student.class_desc }}</td>
                      <td>{{ person.student.campus_desc }}</td>
                      <td>{{ person.student.enrollment_status_desc }}</td>
                      <td>
                        <div
                          v-for="adviser in person.student.advisers"
                          :key="adviser.id"
                        >
                          {{ adviser.uwnetid }}
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-else>no students in your caseload</div>
              </div>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import { markRaw } from "vue";
import { Card, CardHeading } from "axdd-components";
import SearchAdviser from "../components/search-adviser.vue";
import SearchStudent from "../components/search-student.vue";
import AddContact from "../components/add-contact.vue";
import TableLoading from "../components/table-loading.vue";
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";
import ProfileMini from "../components/student/profile-mini.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "profile-mini": ProfileMini,
    "search-adviser": SearchAdviser,
    "search-student": SearchStudent,
    "table-loading": TableLoading,
    "add-contact": AddContact,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  data() {
    return {
      pageTitle: "Caseload",
      isLoading: true,
      // data
      students: [],
      userNetId: document.body.getAttribute("data-user-netid"),
    };
  },
  created: function () {
    this.loadAdviserCaseload(this.userNetId);
  },
  computed: {
    paginationOptions: function () {
      return {
        page_num: this.currentPage,
        page_size: this.pageSize,
      };
    },
    numPages: function () {
      let page = Math.ceil(this.studentsCount / this.pageSize);
      return page > 0 ? page : 1;
    },
  },
  methods: {
    loadAdviserCaseload: function (netid) {
      let _this = this;
      this.getAdviserCaseload(netid).then((response) => {
        _this.persons = response.data;
        console.log(_this.persons);
        _this.isLoading = false;
      });
    },
    showPriorityRing: function (priorityValue) {
      // mocked display
      if (priorityValue == "-3.4") {
        return "border-danger";
      } else if (priorityValue == "2.2") {
        return "border-warning";
      } else {
        return "";
      }
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
