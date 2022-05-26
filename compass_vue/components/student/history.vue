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
            :panel-id="'visit'"
            :active-tab="true"
            >Visit</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'history'" :panel-id="'transcript'"
            >Registrations</axdd-tab-item
          >
          <axdd-tab-item :tabs-id="'history'" :panel-id="'major'"
            >Major</axdd-tab-item
          >
        </template>
        <template #panels>
          <axdd-tab-panel :panel-id="'visit'" :active-panel="true">
            <div class="table-responsive">
              <table class="table table-hover table-striped m-0">
                <thead class="small">
                  <tr>
                    <th>Date</th>
                    <th class="text-nowrap">Location</th>
                    <th>Course</th>
                    <th>Check-in</th>
                    <th>Check-out</th>
                    <th>Duration</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td scope="row">09/23/2020</td>
                    <td>Instructional Center</td>
                    <td>BUS 220</td>
                    <td>10:35am</td>
                    <td>11:42pm</td>
                    <td>1hr 2mins</td>
                  </tr>
                  <tr>
                    <td scope="row">07/04/2020</td>
                    <td>Computer Lab</td>
                    <td>CSE 142</td>
                    <td>9:15am</td>
                    <td>11:2am</td>
                    <td>2 hrs</td>
                  </tr>
                  <tr>
                    <td scope="row">06/29/2020</td>
                    <td>Instruction Center</td>
                    <td>BUS 220</td>
                    <td>4:31pm</td>
                    <td>4:45pm</td>
                    <td>15 mins</td>
                  </tr>
                  <tr>
                    <td scope="row">5/14/2020</td>
                    <td>Instructional Center</td>
                    <td>BUS 220</td>
                    <td>2:34pm</td>
                    <td>6:35pm</td>
                    <td>4 hrs</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </axdd-tab-panel>
          <axdd-tab-panel :panel-id="'transcript'">
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
          <axdd-tab-panel :panel-id="'major'">
            <div class="table-responsive">
              <h3
                class="
                  h6
                  text-uppercase
                  fw-bold
                  text-uppercase
                  axdd-font-encode-sans
                  text-dark-beige
                "
              >
                Accepted Major
              </h3>
              <table class="table table-hover table-striped m-0 mb-3">
                <thead class="small">
                  <tr>
                    <th>Date</th>
                    <th>Major</th>
                    <th>Status</th>
                    <th class="text-nowrap">Source</th>
                    <th>Action</th>
                    <th>Notes</th>
                    <th>User</th>
                  </tr>
                </thead>
                <tbody class="mb-3">
                  <tr>
                    <td scope="row">10/01/2021</td>
                    <td>Psychology</td>
                    <td>Accepted</td>
                    <td>SWS</td>
                    <td></td>
                    <td></td>
                    <td></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="table-responsive">
              <h3
                class="
                  h6
                  text-uppercase
                  fw-bold
                  text-uppercase
                  axdd-font-encode-sans
                  text-dark-beige
                "
              >
                Intended Major
              </h3>
              <table class="table table-hover table-striped m-0 mb-3">
                <thead class="small">
                  <tr>
                    <th>Date</th>
                    <th>Major</th>
                    <th>Status</th>
                    <th class="text-nowrap">Source</th>
                    <th>Action</th>
                    <th>Notes</th>
                    <th>User</th>
                  </tr>
                </thead>
                <tbody class="mb-3">
                  <tr>
                    <td scope="row">9/23/2020</td>
                    <td>Computer Engineering</td>
                    <td>Intended #1</td>
                    <td>DawgPath</td>
                    <td>Remove</td>
                    <td>No longer interested</td>
                    <td>Student</td>
                  </tr>
                  <tr>
                    <td scope="row">7/04/2020</td>
                    <td>Human Centered Design &amp; Engineering</td>
                    <td>Intended #2</td>
                    <td>Compass</td>
                    <td>Add</td>
                    <td>Wants to be a UX Designer</td>
                    <td>Pedro Sanchez</td>
                  </tr>
                  <tr>
                    <td scope="row">6/29/2020</td>
                    <td>Accounting</td>
                    <td>Intended #3</td>
                    <td>Compass</td>
                    <td>Remove</td>
                    <td>Does not like numbers</td>
                    <td>Pedro Sanchez</td>
                  </tr>
                  <tr>
                    <td scope="row">5/23/2020</td>
                    <td>Economics</td>
                    <td>Intended #3</td>
                    <td>DawgPath</td>
                    <td>Remove</td>
                    <td>n/a</td>
                    <td>Student</td>
                  </tr>
                </tbody>
              </table>
              <h3
                class="
                  h6
                  text-uppercase
                  fw-bold
                  text-uppercase
                  axdd-font-encode-sans
                  text-dark-beige
                "
              >
                Intended Major upon Admission
              </h3>
              <table class="table table-hover table-striped m-0">
                <thead class="small">
                  <tr>
                    <th>Date</th>
                    <th>Major</th>
                    <th>Status</th>
                    <th class="text-nowrap">Source</th>
                    <th>Action</th>
                    <th>Notes</th>
                    <th>User</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td scope="row">5/14/2020</td>
                    <td>Informatics</td>
                    <td>Intended #3</td>
                    <td>Admissions</td>
                    <td></td>
                    <td></td>
                    <td></td>
                  </tr>
                  <tr>
                    <td scope="row">5/14/2020</td>
                    <td>Computer Science</td>
                    <td>Intended #2</td>
                    <td>Admissions</td>
                    <td></td>
                    <td></td>
                    <td></td>
                  </tr>
                  <tr>
                    <td scope="row">5/14/2020</td>
                    <td>Anthropolgy</td>
                    <td>Intended #1</td>
                    <td>Admissions</td>
                    <td></td>
                    <td></td>
                    <td></td>
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
