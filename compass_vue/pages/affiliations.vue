// reports.vue

<template>
  <Layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row my-4 small">
        <div class="col">
          <BCard class="bg-body-tertiary rounded-3" border-variant="0">
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
                :disabled="isLoading"
              >
                Process Batch
              </button>
            </div>
          </BCard>
        </div>
      </div>

      <div class="row my-4">
        <div class="col">
          <BCard
            class="shadow-sm rounded-3"
            header-class="p-3"
            header-bg-variant="transparent"
            body-class="p-0"
          >
            <template #header>
              <div class="fs-6 fw-bold">Students</div>
            </template>
            <div v-if="responseData.length !== 0" class="table-responsive m-n3">
              <table class="table m-0">
                <thead class="table-light text-muted small">
                  <tr>
                    <th scope="col" class="ps-3" style="width: 20%">
                      Student Number
                    </th>
                    <th scope="col" style="width: 20%">First</th>
                    <th scope="col">Last</th>
                    <th scope="col">NetID</th>
                    <th scope="col" style="width: 40%">Affiliation Status</th>
                  </tr>
                </thead>
                <tbody v-if="isLoading">
                  <tr v-for="item in 15" :key="item">
                    <td class="placeholder-glow ps-3">
                      <div>
                        <span class="placeholder bg-light-gray col-10"></span>
                      </div>
                    </td>
                    <td class="placeholder-glow">
                      <div>
                        <span class="placeholder bg-light-gray col-10"></span>
                      </div>
                    </td>
                    <td class="placeholder-glow">
                      <div>
                        <span class="placeholder bg-light-gray col-10"></span>
                      </div>
                    </td>
                    <td class="placeholder-glow">
                      <div>
                        <span class="placeholder bg-light-gray col-10"></span>
                      </div>
                    </td>
                    <td class="placeholder-glow">
                      <div>
                        <span class="placeholder bg-light-gray col-10"></span>
                      </div>
                    </td>
                  </tr>
                </tbody>
                <tbody v-else>
                  <template
                    v-for="(person, index) in responseData"
                    :key="index"
                  >
                    <tr v-if="!person.error">
                      <td scope="row" class="ps-3">
                        <router-link
                          :to="{ path: '/student/' + person.student_number }"
                        >
                          {{ person.student_number }}
                        </router-link>
                      </td>
                      <td>{{ person.first_name }}</td>
                      <td>{{ person.surname }}</td>
                      <td>{{ person.uwnetid }}</td>
                      <td>
                        <span
                          class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1 text-bg-success"
                          >Completed</span
                        >
                      </td>
                    </tr>
                    <tr v-else>
                      <td scope="row" class="ps-3">
                        {{ person.student_number }}
                      </td>
                      <td scope="row" colspan="3">
                        {{ person.error }}
                      </td>
                      <td>
                        <span
                          class="small badge rounded-pill border-0 px-2 py-1 mb-0 me-1 text-bg-danger"
                          >Error</span
                        >
                      </td>
                    </tr>
                  </template>
                </tbody>
              </table>
            </div>
            <div v-else class="p-3">You have not uploaded any students.</div>
          </BCard>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import Layout from "@/layout.vue";
import { getAffiliations, uploadStudentAffiliations } from "@/utils/data";
import { getCohorts } from "@/utils/cohorts";
import { BCard } from "bootstrap-vue-next";

export default {
  components: {
    Layout,
    BCard,
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
      isLoading: false,
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
      // immediately show loading placeholder
      this.isLoading = true;

      if (!this.validateForm()) {
        this.isLoading = false;
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
          // MARK: give time for the loading spinner to appear
          setTimeout(() => {
            this.isLoading = false;
          }, 1000);
        })
        .catch((error) => {
          this.isLoading = false;
          alert(error.response.data);
        });
    },
  },
};
</script>
