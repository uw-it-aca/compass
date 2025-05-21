<template>
  <Layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <!-- BCard (Panel) -->
          <BCard class="bg-body-tertiary rounded-3" border-variant="0">
            <div class="row">
              <div class="col-xl-3 me-auto">
                <div class="fw-bold lh-lg">Search all Students:</div>
                <div>
                  <SearchStudent />
                </div>
              </div>
              <div class="col-xl-9">
                <div
                  class="row gy-2 gx-3 align-items-center justify-content-end"
                >
                  <div class="col">
                    <label for="classFilter" class="fw-bold lh-lg"
                      >Class:</label
                    >
                    <select
                      id="classFilter"
                      v-model="selectedClass"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in classOptions"
                        :key="index"
                        :value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>

                  <div class="col">
                    <label for="campusFilter" class="fw-bold lh-lg"
                      >Campus:</label
                    >
                    <select
                      id="campusFilter"
                      v-model="selectedCampus"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in campusOptions"
                        :key="index"
                        :value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>

                  <div class="col">
                    <label for="campusFilter" class="fw-bold lh-lg"
                      >Degree:</label
                    >
                    <select
                      id="campusFilter"
                      v-model="selectedDegree"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in degreeOptions"
                        :key="index"
                        :value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>

                  <div class="col">
                    <label for="scholarshipFilter" class="fw-bold lh-lg"
                      >Acad. Standing:</label
                    >
                    <select
                      id="scholarshipFilter"
                      v-model="selectedScholarship"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in scholarshipOptions"
                        :key="index"
                        :value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>

                  <div class="col">
                    <label for="registrationFilter" class="fw-bold lh-lg"
                      >Registered:</label
                    >
                    <select
                      id="registrationFilter"
                      v-model="selectedRegistration"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in registrationOptions"
                        :key="index"
                        :value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>
                  <div class="col">
                    <label for="holdsFilter" class="fw-bold lh-lg"
                      >Holds:</label
                    >
                    <select
                      id="holdsFilter"
                      v-model="selectedHolds"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in holdsOptions"
                        :key="index"
                      >
                        {{ option.value }}
                        :value="option.id"
                      </option>
                    </select>
                  </div>
                  <div class="col">
                    <label for="holdsFilter" class="fw-bold lh-lg"
                      >Alert Status:</label
                    >
                    <select
                      id="holdsFilter"
                      v-model="selectedAlert"
                      class="form-select form-select-sm"
                    >
                      <option selected :value="undefined">All</option>
                      <option
                        v-for="(option, index) in alertOptions"
                        :key="index"
                        :value="option.id"
                      >
                        {{ option.value }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="text-end mt-3">
                  <button
                    v-if="!unsavedPreferences"
                    disabled
                    type="button"
                    class="btn btn-sm fs-7 btn-outline-dark-beige rounded"
                    @click="saveFilterPreferences"
                  >
                    <i class="bi bi-star-fill me-2"></i>Using saved filters
                  </button>
                  <button
                    v-else
                    type="button"
                    class="btn btn-sm fs-7 btn-outline-dark-beige rounded"
                    @click="saveFilterPreferences"
                  >
                    <i class="bi bi-star me-2"></i>Set filters as default
                  </button>
                </div>
              </div>
            </div>
          </BCard>
        </div>
      </div>

      <div class="row my-4">
        <div class="col">
          <!-- BCard (Default/Header)-->
          <BCard
            class="shadow-sm rounded-3"
            header-class="p-3"
            header-bg-variant="transparent"
            body-class="p-0"
          >
            <template #header>
              <div class="d-flex justify-content-between align-items-center">
                <div class="fs-6 fw-bold">Caseload</div>

                <BDropdown
                  size="sm"
                  variant="link"
                  class="bg-secondary-hover link-primary link-underline link-underline-opacity-0 rounded"
                  no-caret
                >
                  <template #button-content
                    ><i class="bi bi-download"></i
                  ></template>
                  <BDropdownItemButton @click="copyEmailList"
                    ><i class="bi bi-envelope-at-fill me-2 text-dark"></i>Copy
                    student email</BDropdownItemButton
                  >
                  <BDropdownItemButton @click="downloadCSV"
                    ><i class="bi bi-filetype-csv me-2 text-dark"></i>Download
                    student data</BDropdownItemButton
                  >
                </BDropdown>
              </div>
            </template>
            <CaseloadTableLoading v-if="isLoading" />
            <CaseloadTableDisplay
              v-else
              :adviser-net-id="adviserNetId"
              :persons="filteredPersons"
            />
          </BCard>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import SearchStudent from "@/components/search-student.vue";
import CaseloadTableDisplay from "@/components/caseload-table-display.vue";
import CaseloadTableLoading from "@/components/caseload-table-loading.vue";
import Layout from "@/layout.vue";
import { getAdviserCaseload, savePreferences } from "@/utils/data";

import { BCard, BDropdown, BDropdownItemButton } from "bootstrap-vue-next";

export default {
  name: "CaseloadPage",
  components: {
    Layout,
    BCard,
    BDropdown,
    BDropdownItemButton,
    SearchStudent,
    CaseloadTableDisplay,
    CaseloadTableLoading,
  },
  setup() {
    return {
      getAdviserCaseload,
    };
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
      selectedDegree: undefined,
      selectedScholarship: undefined,
      selectedCampus: undefined,
      selectedRegistration: undefined,
      selectedHolds: undefined,
      selectedAlert: undefined,
      degreeOptions: [
        { id: "ADMINISTRATIVE HOLD", value: "Hold" },
        { id: "INCOMPLETE", value: "Incomplete" },
        { id: "APPLIED", value: "Applied" },
        { id: "GRANTED", value: "Granted" },
        { id: "none", value: "None" },
      ],
      scholarshipOptions: [
        { id: 1, value: "Dean's List" },
        { id: 4, value: "Acad. Alert" },
        { id: 3, value: "Acad. Warning" },
        { id: 0, value: "None" },
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
        { id: true, value: "Yes" },
        { id: false, value: "No" },
      ],
      holdsOptions: [
        { id: true, value: "Yes" },
        { id: false, value: "No" },
      ],
      alertOptions: [
        { id: "danger", value: "Red" },
        { id: "warning", value: "Yellow" },
        { id: "success", value: "Green" },
      ],
      saveCount: 0,
      errorResponse: null,
    };
  },

  computed: {
    filteredPersons: function () {
      let filteredPersons = this.persons;
      if (this.selectedClass) {
        filteredPersons = filteredPersons.filter((person) => {
          return person.class_desc === this.selectedClass;
        });
      }
      if (this.selectedDegree) {
        filteredPersons = filteredPersons.filter((person) => {
          try {
            return (
              person.latest_degree.degree_status_desc === this.selectedDegree
            );
          } catch (error) {
            try {
              return (
                person.latest_degree === null && this.selectedDegree === "none"
              );
            } catch (error) {
              return false;
            }
          }
        });
      }
      if (this.selectedScholarship !== undefined) {
        filteredPersons = filteredPersons.filter((person) => {
          try {
            return (
              person.latest_transcript.scholarship_type ===
              this.selectedScholarship
            );
          } catch (error) {
            return false;
          }
        });
      }
      if (this.selectedCampus) {
        filteredPersons = filteredPersons.filter(
          (person) => person.campus_desc === this.selectedCampus
        );
      }
      if (this.selectedRegistration !== undefined) {
        filteredPersons = filteredPersons.filter(
          (person) => person.registered_in_quarter === this.selectedRegistration
        );
      }
      if (this.selectedHolds !== undefined) {
        filteredPersons = filteredPersons.filter(
          (person) => person.registration_hold_ind === this.selectedHolds
        );
      }
      if (this.selectedAlert !== undefined) {
        filteredPersons = filteredPersons.filter(
          (person) => person.analytics_alert === this.selectedAlert
        );
      }
      return filteredPersons;
    },
    unsavedPreferences: function () {
      // Reference saveCount to trigger re-compute on save
      this.saveCount;

      let caseload_filter_prefs = {};
      if ("caseload_filters" in window.userPreferences) {
        caseload_filter_prefs = window.userPreferences.caseload_filters;
      }
      return (
        this.selectedClass !== (caseload_filter_prefs.class || undefined) ||
        this.selectedCampus !== (caseload_filter_prefs.campus || undefined) ||
        this.selectedDegree !== (caseload_filter_prefs.degree || undefined) ||
        this.selectedScholarship !==
          (caseload_filter_prefs.scholarship || undefined) ||
        this.selectedRegistration !==
          (caseload_filter_prefs.registered !== undefined
            ? this.getBooleanFromString(caseload_filter_prefs.registered)
            : undefined) ||
        this.selectedHolds !==
          (caseload_filter_prefs.holds !== undefined
            ? this.getBooleanFromString(caseload_filter_prefs.holds)
            : undefined) ||
        this.selectedAlert !== (caseload_filter_prefs.alert || undefined)
      );
    },
  },
  created: function () {
    // setup() exposed properties can be accessed on `this`
    this.loadAdviserCaseload(this.adviserNetId);
    this.loadFilterPreferences();
  },
  methods: {
    copyEmailList: function () {
      let email_list = [];
      this.filteredPersons.forEach((person) => {
        email_list.push(person.uwnetid + "@uw.edu");
      });
      // copy to clipboard
      navigator.clipboard.writeText(email_list.join("; "));
    },
    downloadCSV: function () {
      let csv_string = "",
        hiddenElement = document.createElement("a"),
        header = [
          "Student Name",
          "Student Number",
          "UW NetID",
          "Email",
          "Class",
          "Campus",
          "Alert Status",
          "Degree Status",
          "Academic Standing",
          "Registered",
          "Holds",
        ],
        timestamp = Math.round(Date.now() / 1000);
      csv_string += header.join(",") + "\n";
      this.filteredPersons.forEach((person) => {
        let alert_status =
          {
            danger: "Red",
            warning: "Yellow",
            success: "Green",
          }[person.analytics_alert] || "";
        let row = [
          person.person__display_name,
          person.student_number,
          person.person__uwnetid,
          person.person__uwnetid + "@uw.edu",
          person.class_desc,
          person.campus_desc,
          alert_status,
          person.latest_degree
            ? person.latest_degree.degree_status_desc
            : undefined,
          person.latest_transcript
            ? person.latest_transcript.scholarship_desc
            : undefined,
          person.registered_in_quarter,
          person.registration_hold_ind,
        ];
        csv_string += row.join(",") + "\n";
      });
      hiddenElement.href =
        "data:text/csv;charset=utf-8," + encodeURI(csv_string);
      hiddenElement.target = "_blank";
      hiddenElement.download = "caseload" + timestamp + ".csv";
      hiddenElement.click();
    },
    capitalizeFirstLetter: function (string) {
      string = string.toLowerCase();
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    loadAdviserCaseload: function (netid) {
      this.isLoading = true;
      this.getAdviserCaseload(netid).then((response) => {
        if (response) {
          this.persons = response;
        }
      })
      .catch((error) => {
        this.errorResponse = error.data;
      })
      .finally(() => {
        this.isLoading = false;
      });
    },
    showPriorityRing: function (priorityValue) {
      // mocked display
      if (priorityValue === "-3.4") {
        return "border-danger";
      } else if (priorityValue === "2.2") {
        return "border-warning";
      } else {
        return "";
      }
    },
    saveFilterPreferences: function () {
      console.log("save", this.selectedAlert);
      savePreferences({
        caseload_filters: {
          class: this.selectedClass,
          campus: this.selectedCampus,
          degree: this.selectedDegree,
          scholarship: this.selectedScholarship,
          registered: this.selectedRegistration,
          holds: this.selectedHolds,
          alert: this.selectedAlert,
        },
      });
      // Update window.userPreferences
      window.userPreferences.caseload_filters = {
        class: this.selectedClass,
        campus: this.selectedCampus,
        degree: this.selectedDegree,
        scholarship: this.selectedScholarship,
        registered:
          this.selectedRegistration === undefined
            ? undefined
            : this.selectedRegistration
              ? "True"
              : "False",
        holds:
          this.selectedHolds === undefined
            ? undefined
            : this.selectedHolds
              ? "True"
              : "False",
        alert: this.selectedAlert,
      };
      // Counter to trigger re-compute on unsavedPreferences
      this.saveCount++;
    },
    loadFilterPreferences: function () {
      let user_prefs = window.userPreferences;
      if (user_prefs.caseload_filters) {
        this.selectedClass = user_prefs.caseload_filters.class;
        this.selectedCampus = user_prefs.caseload_filters.campus;
        this.selectedDegree = user_prefs.caseload_filters.degree;
        this.selectedScholarship = user_prefs.caseload_filters.scholarship;
        this.selectedRegistration = this.getBooleanFromString(
          user_prefs.caseload_filters.registered
        );
        this.selectedHolds = this.getBooleanFromString(
          user_prefs.caseload_filters.holds
        );
        this.selectedAlert = user_prefs.caseload_filters.alert;
      }
    },
    getBooleanFromString: function (string) {
      if (string === "True") {
        return true;
      } else if (string === "False") {
        return false;
      } else {
        return undefined;
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
