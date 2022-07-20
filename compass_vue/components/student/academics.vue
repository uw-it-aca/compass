<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Academics</axdd-card-heading>
      <axdd-card-tabs>
        <axdd-tabs-list :tabs-id="'history'" :variant="'pills'" class="small">
          <template #items>
            <axdd-tabs-item
              :tabs-id="'history'"
              :panel-id="'major'"
              :active-tab="true"
              :variant="'pills'"
              >Current</axdd-tabs-item
            >
            <axdd-tabs-item :tabs-id="'history'" :panel-id="'transcript'" :variant="'pills'"
              >Unofficial Transcript</axdd-tabs-item
            >
          </template>
        </axdd-tabs-list>
      </axdd-card-tabs>
    </template>
    <template #body>
      <axdd-tabs-display :tabs-id="'history'">
        <template #panels>
          <axdd-tabs-panel :panel-id="'major'" :active-panel="true">
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
                  <li>
                    Total UW Credits: {{ person.student.total_uw_credits }}
                  </li>
                  <li>
                    Transfer credits:
                    <span class="text-danger">tbd</span>
                  </li>
                </ul>
              </div>
              <div class="flex-fill small">
                <div class="mb-3">
                  Current Majors:

                  <div
                    v-for="(major, index) in person.student.majors"
                    :key="index"
                  >
                    {{ major.major_abbr_code }}, {{ major.major_name }}
                  </div>
                </div>
                <div>
                  Desired Majors (3 upon admission):
                  <div
                    v-for="(intendedMajor, index) in person.student
                      .intended_majors"
                    :key="index"
                  >
                    {{ intendedMajor.major_abbr_code }},
                    {{ intendedMajor.major_name }}
                  </div>
                </div>
              </div>
            </div>
          </axdd-tabs-panel>

          <axdd-tabs-panel :panel-id="'transcript'">
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
                    <div class="border-top mt-3">
                      Special Program Code:
                      <template v-if="person.student.transcripts">
                        {{ person.student.transcripts[0].special_program }}
                      </template>
                    </div>
                    <div>
                      Scholarships: <span class="text-danger">tbd</span>
                    </div>
                    <div>
                      Yearly Honors: <span class="text-danger">tbd</span>
                    </div>
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
                    <div class="border-top mt-3">
                      Special Program Code:
                      <template v-if="person.student.transcripts">
                        {{ person.student.transcripts[0].special_program }}
                      </template>
                    </div>
                    <div>
                      Scholarships: <span class="text-danger">tbd</span>
                    </div>
                    <div>
                      Yearly Honors: <span class="text-danger">tbd</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </axdd-tabs-panel>
        </template>
      </axdd-tabs-display>
    </template>
  </axdd-card>
</template>

<script>
import {
  Card,
  CardTabs,
  CardHeading,
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";

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
    "axdd-card-tabs": CardTabs,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
  },
  data() {
    return {};
  },
};
</script>
