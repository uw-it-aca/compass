<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">History</axdd-card-heading>
    </template>
    <template #body>
      <axdd-tabs :tabs-id="'history'">
        <template #items>
          <axdd-tab-item
            :tabs-id="'history'"
            :panel-id="'major'"
            :active-tab="true"
            >Majors</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'history'" :panel-id="'transcript'"
            >Unoffical Transcript (sws)</axdd-tab-item
          >
        </template>
        <template #panels>
          <axdd-tab-panel :panel-id="'major'" :active-panel="true">
            <div class="table-responsive">
              <h3
                class="h6 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
              >
                Majors
              </h3>
              <table class="table table-hover table-striped m-0 mb-5">
                <thead class="small">
                  <tr>
                    <th>Code</th>
                    <th class="w-50">Major</th>
                    <th>Status</th>
                    <th class="text-nowrap">Source</th>
                  </tr>
                </thead>
                <tbody class="mb-3">
                  <tr
                    v-for="(major, index) in person.student.majors"
                    :key="index"
                  >
                    <td>{{ major.major_abbr_code }}</td>
                    <td>{{ major.major_name }}</td>
                    <td>Current</td>
                    <td>EDW/UWPDS</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="table-responsive">
              <h3
                class="h6 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
              >
                Intended Major (compass)
              </h3>
              <table class="table table-hover table-striped m-0 mb-5">
                <thead class="small">
                  <tr>
                    <th>Code</th>
                    <th class="w-50">Major</th>
                    <th>Status</th>
                    <th class="text-nowrap">Source</th>
                  </tr>
                </thead>
                <tbody class="mb-3">
                  <tr>
                    <td>ENG</td>
                    <td>Computer Engineering</td>
                    <td>Intended</td>
                    <td>DawgPath</td>
                  </tr>
                  <tr>
                    <td>HCDE</td>
                    <td>Human Centered Design &amp; Engineering</td>
                    <td>Intended</td>
                    <td>Compass</td>
                  </tr>
                  <tr>
                    <td>ACCT</td>
                    <td>Accounting</td>
                    <td>Intended</td>
                    <td>Compass</td>
                  </tr>
                  <tr>
                    <td>ECON</td>
                    <td>Economics</td>
                    <td>Intended</td>
                    <td>DawgPath</td>
                  </tr>
                </tbody>
              </table>
              <h3
                class="h6 text-uppercase fw-bold text-uppercase axdd-font-encode-sans text-dark-beige"
              >
                Intended Major upon Admission to UW
              </h3>
              <table class="table table-hover table-striped m-0">
                <thead class="small">
                  <tr>
                    <th>Code</th>
                    <th class="w-50">Major</th>
                    <th>Status</th>
                    <th class="text-nowrap">Source</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(intendedMajor, index) in person.student
                      .intended_majors"
                    :key="index"
                  >
                    <td>{{ intendedMajor.major_abbr_code }}</td>
                    <td>{{ intendedMajor.major_name }}</td>
                    <td>Intended</td>
                    <td>EDW/UWPDS</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </axdd-tab-panel>

          <axdd-tab-panel :panel-id="'transcript'">
            <p class="text-danger small">
              Previous Registrations and Grade transcript
            </p>
            <div class="table-responsive">
              <table class="table table-hover table-striped m-0">
                <thead class="small">
                  <tr>
                    <th>Course</th>
                    <th>Credits</th>
                    <th>Grade</th>
                    <th>Year</th>
                    <th>Quarter</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>BIOL 350</td>
                    <td>3</td>
                    <td>3.8</td>
                    <td>2021</td>
                    <td>Spring</td>
                  </tr>
                  <tr>
                    <td>CHEM 238</td>
                    <td>4</td>
                    <td>4.0</td>
                    <td>2021</td>
                    <td>Autumn</td>
                  </tr>
                  <tr>
                    <td>MATH 210</td>
                    <td>5.0</td>
                    <td>W4</td>
                    <td>2021</td>
                    <td>Autumn</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </axdd-tab-panel>
        </template>
      </axdd-tabs>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading, Tabs, TabItem, TabPanel } from "axdd-components";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-tabs": Tabs,
    "axdd-tab-item": TabItem,
    "axdd-tab-panel": TabPanel,
  },
  data() {
    return {};
  },
};
</script>
