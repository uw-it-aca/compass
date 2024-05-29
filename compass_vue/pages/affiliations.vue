// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <div class="bg-light p-3 rounded-3">
            <div class="d-flex">
              <div class="me-3">
                <label for="formFile" class="form-label fw-bold"
                  >Upload students</label
                >
                <input
                  class="form-control form-control-sm"
                  type="file"
                  id="formFile"
                  @change="addFile"
                />
              </div>
              <div class="me-3">
                <label for="formAffiliation" class="form-label fw-bold"
                  >Select affiliations</label
                >
                <select
                  id="formAffiliation"
                  name="affiliation"
                  class="form-select form-select-sm"
                  aria-label="Select affiliation"
                  @change="addAffliation"
                >
                  <option selected disabled :value="undefined">
                    Choose one...
                  </option>
                  <template
                    v-for="affiliation in affiliations"
                    :key="affiliation.id"
                  >
                    <option :value="affiliation.id">
                      {{ affiliation.name }}
                    </option>
                  </template>
                </select>
              </div>
              <div>
                <label for="formCohort" class="form-label fw-bold"
                  >Select cohort</label
                >
                <select
                  id="formCohort"
                  name="cohort"
                  class="form-select form-select-sm"
                  aria-label="Select cohort"
                  @change="addCohort"
                >
                  <option selected disabled :value="undefined">
                    Choose one...
                  </option>
                  <template v-for="(cohort, index) in cohorts" :key="index">
                    <option :value="cohort.start_year + '-' + cohort.end_year">
                      {{ cohort.start_year }}-{{ cohort.end_year }}
                    </option>
                  </template>
                </select>
              </div>
            </div>
            <div class="text-end">
              <button
                type="button"
                class="btn btn-sm fs-7 btn-outline-dark-beige rounded"
                @click="processUpload"
              >
                Process Batch
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="responseData.length !== 0" class="row my-4">
        <div class="col">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Student Number</th>
                <th scope="col">First</th>
                <th scope="col">Last</th>
                <th scope="col">NetID</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(person, index) in responseData" :key="index">
                <tr v-if="!person.error">
                  <td scope="row">{{ person.student_number }}</td>
                  <td>{{ person.first_name }}</td>
                  <td>{{ person.last_name }}</td>
                  <td>{{ person.uwnetid }}</td>
                  <td>Updated</td>
                </tr>
                <tr v-else>
                  <td scope="row" colspan="5" class="text-end">{{ person.error }}</td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else>You have not uploaded any students yet.</div>
    </template>
  </layout>
</template>

<script>
import Layout from "@/layout.vue";
import { getAffiliations, uploadStudentAffiliations } from "@/utils/data";
import { getCohorts } from "@/utils/cohorts";

export default {
  components: {
    layout: Layout,
  },
  props: {
    cohortCount: {
      type: Number,
      default: 5,
    },
  },
  setup() {
    return {
      getAffiliations,
      uploadStudentAffiliations,
    };
  },
  data() {
    return {
      pageTitle: "Upload Batch Affiliations",
      isLoading: true,
      affiliations: [],
      cohorts: getCohorts(this.cohortCount),
      file: null,
      affiliationId: null,
      cohortName: null,
      responseData: [],
    };
  },
  created: function () {
    this.loadAffiliations();
  },
  methods: {
    addFile(e) {
      this.file = e.target.files[0];
    },
    addAffliation(e) {
      this.affiliationId = e.target.value;
    },
    addCohort(e) {
      this.cohortName = e.target.value;
    },
    loadAffiliations() {
      this.getAffiliations().then((response) => {
        if (response.data) {
          this.affiliations = response.data;
        }
      });
    },
    validateForm() {
      let is_invalid = false;
      if (this.file === null) {
        is_invalid = true;
      }
      if (this.affiliationId === null) {
        is_invalid = true;
      }
      if (this.cohortName === null) {
        is_invalid = true;
      }
      return !is_invalid;
    },
    processUpload() {
      if (!this.validateForm()) {
        alert(
          "Missing form values: affiliationId=" +
            this.affiliationId +
            ", cohortName=" +
            this.cohortName +
            ", file=" +
            this.file
        );
        return;
      }
      this.uploadStudentAffiliations(
        this.affiliationId,
        this.file,
        this.cohortName
      )
        .then((response) => {
          this.responseData = response.data;
        })
        .catch((error) => {
          alert(error.response.data);
        });
    },
  },
};
</script>
