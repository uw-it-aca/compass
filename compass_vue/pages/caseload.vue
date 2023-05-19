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
                    <label for="enrollmentFilter">Enrollment:</label>
                    <select id="enrollmentFilter" v-model="selectedEnrollment" class="">
                      <option selected :value="undefined">All</option>
                      <option v-for="option in enrollmentOptions" v-bind:value="option.id">
                        {{ option.value }}
                      </option>
                    </select>
                    <label for="classFilter">Class:</label>
                    <select id="classFilter" v-model="selectedClass" class="">
                      <option selected :value="undefined">All</option>
                      <option v-for="option in classOptions" v-bind:value="option.id">
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
      selectedEnrollment: undefined,
      selectedClass: undefined,
    };
  },
  created: function () {
    this.loadAdviserCaseload(this.adviserNetId);
  },
  computed: {
    enrollmentOptions: function(){
      let unique_values = [],
        value_objs = [];
      this.persons.forEach((person) =>{
        if(!unique_values.includes(person.student.enroll_status_desc)){
          unique_values.push(person.student.enroll_status_desc);
          value_objs.push({"id": person.student.enroll_status_desc,
            "value": this.capitalizeFirstLetter(person.student.enroll_status_desc)})
        }
      });
      return value_objs;
    },
    classOptions: function(){
      let unique_values = [],
        value_objs = [];
      this.persons.forEach((person) =>{
        if(!unique_values.includes(person.student.class_code)){
          unique_values.push(person.student.class_code);
          value_objs.push({"id": person.student.class_code,
            "value": person.student.class_desc})
        }
      });
      return value_objs;
    },
    filteredPersons: function () {
      let filteredPersons = this.persons;
      if (this.selectedEnrollment) {
        filteredPersons = filteredPersons.filter(
          (person) => person.student.enroll_status_desc == this.selectedEnrollment
        );
      }
      if (this.selectedClass) {
        filteredPersons = filteredPersons.filter(
          (person) => person.student.class_code == this.selectedClass
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
