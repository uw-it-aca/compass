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
            <axdd-tabs-item
              :tabs-id="'history'"
              :panel-id="'transcript'"
              :variant="'pills'"
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
                <ul class="list-unstyled">
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
                  <li>
                    Current Majors:
                    <ul>
                      <li
                        v-for="(major, index) in person.student.majors"
                        :key="index"
                      >
                        {{ major.major_abbr_code }}, {{ major.major_name }}
                      </li>
                    </ul>
                  </li>
                  <li>
                    Desired Majors (upon admission):
                    <ul>
                      <li
                        v-for="(intendedMajor, index) in person.student
                          .intended_majors"
                        :key="index"
                      >
                        {{ intendedMajor.major_abbr_code }},
                        {{ intendedMajor.major_name }}
                      </li>
                    </ul>
                  </li>
                </ul>
              </div>
              <div class="flex-fill">
                <ul class="list-unstyled">
                  <li>Total Credits: {{ person.student.total_credits }}</li>
                  <li>
                    Total UW Credits: {{ person.student.total_uw_credits }}
                  </li>
                  <li>
                    Total Deductible Credits:
                    {{ person.student.total_deductible_credits }}
                  </li>
                  <li>
                    Total Extension Credits:
                    {{ person.student.total_extension_credits }}
                  </li>
                  <li>
                    Total Non-Graded Credits:
                    {{ person.student.total_non_graded_credits }}
                  </li>
                  <li>
                    Total Registered Credits:
                    {{ person.student.total_registered_credits }}
                  </li>
                  <li>
                    Total Transfer Credits:
                    {{ person.student.total_transfer_credits }}
                  </li>
                  <li>
                    Total Lower Division Transfer Credits:
                    {{ person.student.total_lower_div_transfer_credits }}
                  </li>
                  <li>
                    Total Upper Division Transfer Credits:
                    {{ person.student.total_upper_div_transfer_credits }}
                  </li>
                </ul>
              </div>
            </div>
          </axdd-tabs-panel>

          <axdd-tabs-panel :panel-id="'transcript'">
            <div class="table-responsive mx-n3 mb-n3">
              <table class="table table-striped table-borderless m-0">
                <thead class="table-light">
                  <tr>
                    <th class="ps-3">Course</th>
                    <th>Title</th>
                    <th>Credits</th>
                    <th>Grade</th>
                    <th class="text-nowrap">For Credit</th>
                  </tr>
                </thead>
                <template
                  v-for="(transcript, transIndex) in transcripts"
                  :key="transIndex"
                >
                  <tbody v-if="transcript.class_schedule">
                    <tr>
                      <td colspan="5" class="fw-bold ps-3">
                        {{ transcript.class_schedule.term.quarter }}
                        {{ transcript.class_schedule.term.year }}
                      </td>
                    </tr>
                    <tr
                      v-for="(section, index3) in transcript.class_schedule
                        .sections"
                      :key="index3"
                    >
                      <td class="ps-3">
                        {{ section.curriculum_abbr }}
                        {{ section.course_number }}
                      </td>
                      <td>{{ section.course_title }}</td>
                      <td>{{ section.credits }}</td>
                      <td>{{ section.grade }}</td>
                      <td>{{ section.for_credit }}</td>
                    </tr>
                    <tr>
                      <td colspan="5" class="text-end">
                        <div>
                          QTR ATTEMPTED: {{ transcript.qtr_graded_attmp }} QTR
                          EARNED: {{ transcript.qtr_grade_points }}
                        </div>
                        <div class="row">
                          <div class="col">
                            <div>
                              Class Code:
                              {{ transcript.special_program }}
                            </div>
                            <div>
                              Enrollment Status: {{ transcript.enroll_status }}
                            </div>
                            <div>
                              Exemption Code: {{ transcript.exemption_code }}
                            </div>
                            <div>Grad status: {{ transcript.grad_status }}</div>
                            <div>
                              Honors Program: {{ transcript.honors_program }}
                            </div>
                          </div>
                          <div class="col">
                            <div>
                              Number Courses: {{ transcript.num_courses }}
                            </div>
                            <div>
                              Scholarships: {{ transcript.scholarship_type }}
                            </div>
                            <div>
                              Special Program Code:
                              {{ transcript.special_program }}
                            </div>
                            <div>Veteran: {{ transcript.veteran }}</div>
                            <div>
                              Veteran Benefit: {{ transcript.veteran_benefit }}
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </table>
            </div>
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

import dataMixin from "../../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
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
    return {
      transcripts: {},
    };
  },
  created() {
    this.loadStudentTranscripts();
  },
  methods: {
    loadStudentTranscripts: function () {
      this.getStudentTranscripts(this.person.uwregid).then((response) => {
        if (response.data) {
          this.transcripts = response.data;
        }
      });
    },
  },
};
</script>
