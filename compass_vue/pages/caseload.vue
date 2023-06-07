<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-light p-3 rounded-3">
            <div class="row">
              <div class="col-xl-4 ms-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <search-student></search-student>
                  <div>
                    <label for="classFilter">Class:</label>
                    <select id="classFilter" v-model="selectedClass" class="">
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="option in classOptions"
                        v-bind:value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                    <label for="scholarshipFilter">Scholarship:</label>
                    <select
                      id="scholarshipFilter"
                      v-model="selectedScholarship"
                      class=""
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="option in scholarshipOptions"
                        v-bind:value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                    <label for="campusFilter">Campus:</label>
                    <select id="campusFilter" v-model="selectedCampus" class="">
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="option in campusOptions"
                        v-bind:value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                    <label for="registrationFilter">Registration Status:</label>
                    <select
                      id="registrationFilter"
                      v-model="selectedRegistration"
                      class=""
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="option in registrationOptions"
                        v-bind:value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                    <label for="holdsFilter">Holds Status:</label>
                    <select id="holdsFilter" v-model="selectedHolds" class="">
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="option in holdsOptions"
                        v-bind:value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="col-4"></div>
              <div class="col-4"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2">Caseload</axdd-card-heading>
            </template>
            <template #body>
              <table-loading v-if="isLoading"></table-loading>
              <table-display
                v-else
                :adviser-net-id="adviserNetId"
                :persons="filteredPersons"
              ></table-display>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import SearchStudent from "../components/search-student.vue";
import CaseloadTableDisplay from "../components/caseload-table-display.vue";
import CaseloadTableLoading from "../components/caseload-table-loading.vue";
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    "search-student": SearchStudent,
    "table-display": CaseloadTableDisplay,
    "table-loading": CaseloadTableLoading,
  },
  data() {
    return {
      pageTitle: "Caseload",
      isLoading: true,
      // data
      persons: [],
      adviserNetId: this.$route.params.id
        ? this.$route.params.id
        : document.body.getAttribute("data-user-override")
        ? document.body.getAttribute("data-user-override")
        : document.body.getAttribute("data-user-netid"),
      selectedClass: undefined,
      selectedScholarship: undefined,
      selectedCampus: undefined,
      selectedRegistration: undefined,
      selectedHolds: undefined,
      scholarshipOptions: [
        { id: 1, value: "Dean's List" },
        { id: 4, value: "Academic Warning" },
        { id: 3, value: "Academic Probation" },
      ],
      classOptions: [
        { id: "Freshman", value: "Freshman" },
        { id: "Sophomore", value: "Sophomore" },
        { id: "Junior", value: "Junior" },
        { id: "Senior", value: "Senior" },
      ],
      campusOptions: [
        { id: "Seattle", value: "Seattle" },
        { id: "Tacoma", value: "Tacoma" },
        { id: "Bothell", value: "Bothell" },
      ],
      registrationOptions: [
        { id: true, value: "Registered" },
        { id: false, value: "Not Registered" },
      ],
      holdsOptions: [
        { id: true, value: "Has Holds" },
        { id: false, value: "No Holds" },
      ],
    };
  },
  created: function () {
    this.loadAdviserCaseload(this.adviserNetId);
  },
  computed: {
    filteredPersons: function () {
      let filteredPersons = this.persons;
      if (this.selectedClass) {
        filteredPersons = filteredPersons.filter((person) => {
          return person.student.class_desc === this.selectedClass;
        });
      }
      if (this.selectedScholarship) {
        filteredPersons = filteredPersons.filter((person) => {
          try {
            return (
              person.student.transcripts[0].scholarship_type ===
              this.selectedScholarship
            );
          } catch (error) {
            return false;
          }
        });
      }
      if (this.selectedCampus) {
        filteredPersons = filteredPersons.filter(
          (person) => person.student.campus_desc === this.selectedCampus
        );
      }
      if (this.selectedRegistration !== undefined) {
        filteredPersons = filteredPersons.filter(
          (person) =>
            person.student.registered_in_quarter === this.selectedRegistration
        );
      }
      if (this.selectedHolds !== undefined) {
        filteredPersons = filteredPersons.filter(
          (person) =>
            person.student.registration_hold_ind === this.selectedHolds
        );
      }
      return filteredPersons;
    },
  },
  methods: {
    capitalizeFirstLetter: function (string) {
      string = string.toLowerCase();
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    loadAdviserCaseload: function (netid) {
      this.getAdviserCaseload(netid).then((response) => {
        this.persons = response.data;
        this.isLoading = false;
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
  tbody tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
