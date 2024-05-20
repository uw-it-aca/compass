// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <h2>Upload Batch Affiliations</h2>

      <div class="row my-4 small">
        <div class="col">
          <div class="bg-light p-3 rounded-3">
            <div class="d-flex">
              <div class="me-3">
                <label for="formFile" class="form-label fw-bold"
                  >Select students</label
                >
                <input class="form-control" type="file" id="formFile" />
              </div>
              <div class="me-3">
                <p>Select Affliations</p>
                <select name="affiliation" class="form-select" aria-label="Select affiliation">
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
                <p>Select Cohort</p>
                <select name="cohort" class="form-select" aria-label="Select cohort">
                  <option selected disabled :value="undefined">
                    Choose one...
                  </option>
                  <template
                    v-for="(cohort, index) in cohorts"
                    :key="index"
                  >
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

      <div class="row my-4">
        <div class="col">
          <p>Upload resulsts...</p>
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
              <tr>
                <th scope="row">2310335</th>
                <td>Louis</td>
                <td>King</td>
                <td>lking</td>
                <td>Uploaded</td>
              </tr>
              <tr>
                <th scope="row">3776803</th>
                <td>Nellie</td>
                <td>Woods</td>
                <td>nwoods</td>
                <td>Uploaded</td>
              </tr>
              <tr>
                <th scope="row">6640182</th>
                <td>Jeffery</td>
                <td>Bridges</td>
                <td>jeffbridges</td>
                <td>error</td>
              </tr>
              <tr>
                <th scope="row">1776982</th>
                <td>Cecelia</td>
                <td>Glover</td>
                <td>ceceglove</td>
                <td>Uploaded</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "@/layout.vue";
import { getAffiliations } from "@/utils/data";
import { getCohorts } from "@/utils/cohorts";

export default {
  components: {
    layout: Layout,
  },
  setup() {
    return {
      getAffiliations,
    };
  },
  data() {
    return {
      pageTitle: "Affiliations",
      isLoading: true,
      affiliations: [],
      cohorts: getCohorts(5),
    };
  },
  created: function () {
    this.loadAffiliations();
  },
  methods: {
    loadAffiliations() {
      this.getAffiliations().then((response) => {
        if (response.data) {
          this.affiliations = response.data;
        }
      });
    },
    processUpload: function () {
      alert("jfsdalkj");
    },
  },
};
</script>
