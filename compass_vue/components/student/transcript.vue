<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Transcript</axdd-card-heading>
    </template>
    <template #body>
      <div class="d-flex">
        <div class="flex-fill">
          <ul class="list-unstyled small">
            <li>
              Enrollment Status:
              <template v-if="person.student.registered_in_quarter">
                Registered
              </template>
              <template v-else> Unregistered </template
              >{{ person.student.enrollment_desc }}
            </li>
            <li>Class standing: {{ person.student.class_desc }}</li>
            <li>GPA: {{ person.student.cumulative_gpa }}</li>
          </ul>
        </div>
        <div class="flex-fill">
          <ul class="list-unstyled small">
            <li>Total Credits: {{ person.student.total_credits }}</li>
            <li>Total UW Credits: {{ person.student.total_uw_credits }}</li>
            <li>
              Transfer credits:
              <span class="text-danger">tbd</span>
            </li>
          </ul>
        </div>
        <div class="flex-fill">
          <ul class="list-unstyled small">
            <li>Scholarships: <span class="text-danger">tbd</span></li>
            <li>Yearly Honors: <span class="text-danger">tbd</span></li>
          </ul>
        </div>
      </div>

      <h3
        class="h6 m-0 text-uppercase fw-bold text-uppercase axdd-font-encode-sans"
      >
        History
      </h3>
      <axdd-tabs :tabs-id="'history'">
        <template #items>
          <axdd-tab-item
            :tabs-id="'history'"
            :panel-id="'major'"
            :active-tab="true"
            >Majors</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'history'" :panel-id="'transcript'"
            >Grades</axdd-tab-item
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
            <table class="table m-0">
              <thead class="small">
                <tr>
                  <th>Course</th>
                  <th class="w-50">Title</th>
                  <th>Credits</th>
                  <th class="text-nowrap">Grade</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colspan="4" class="fw-bold bg-light">Autumn 1995</td>
                </tr>
                <tr>
                  <td>ANTH 100</td>
                  <td>Intro to Anthropology</td>
                  <td>5.0</td>
                  <td>3.2</td>
                </tr>
                <tr>
                  <td>ENG 104</td>
                  <td>Introductory Composition</td>
                  <td>5.0</td>
                  <td>3.3</td>
                </tr>
                <tr>
                  <td>MATH 102</td>
                  <td>Algebra</td>
                  <td>5.0</td>
                  <td>2.6</td>
                </tr>
                <tr>
                  <td colspan="4" class="text-end small">
                    <div>QTR ATTEMPTED: 15.0 EARNED: 15.0 GPA: 3.03</div>
                    <div>QTR GRADED AT: 15.0 GRADE POINTS: 45.5</div>
                    <div>
                      CUM ATTEMPTED: 15.0 UW EARNED: 15.0 TTL EARNED: 15.0
                    </div>
                    <div>CUM GRADED AT: 15.0 GRADE PTS: 45.5 CUM GPA: 3.03</div>
                  </td>
                </tr>
              </tbody>
              <!-- new quarter -->
              <tbody>
                <tr>
                  <td colspan="4" class="fw-bold bg-light">Winter 1995</td>
                </tr>
                <tr>
                  <td>AAS 206</td>
                  <td>Contemporary Problems Asian American History</td>
                  <td>5.0</td>
                  <td>2.5</td>
                </tr>
                <tr>
                  <td>ENG 105</td>
                  <td>Introductory Composition</td>
                  <td>5.0</td>
                  <td>3.3</td>
                </tr>
                <tr>
                  <td>MATH 103</td>
                  <td>Introduction Elementary Function</td>
                  <td>5.0</td>
                  <td>3.2</td>
                </tr>
                <tr>
                  <td colspan="4" class="text-end small">
                    <div>QTR ATTEMPTED: 15.0 EARNED: 15.0 GPA: 2.17</div>
                    <div>QTR GRADED AT: 15.0 GRADE POINTS: 32.5</div>
                    <div>
                      CUM ATTEMPTED: 30.0 UW EARNED: 30.0 TTL EARNED: 30.0
                    </div>
                    <div>CUM GRADED AT: 30.0 GRADE PTS: 78.0 CUM GPA: 2.60</div>
                  </td>
                </tr>
              </tbody>
            </table>
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
