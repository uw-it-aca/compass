<template>
  <axdd-card>
    <template #heading-action>
      <axdd-card-heading :level="2">Unofficial Transcript</axdd-card-heading>
    </template>
    <template #body>
      <div class="table-responsive border-top mx-n3 mb-n3">
        <table class="table m-0">
          <thead class="table-light text-muted small">
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
                v-for="(section, index3) in transcript.class_schedule.sections"
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
                    QTR ATTEMPTED: {{ transcript.qtr_graded_attmp }} QTR EARNED:
                    {{ transcript.qtr_grade_points }}
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
                      <div>Exemption Code: {{ transcript.exemption_code }}</div>
                      <div>Grad status: {{ transcript.grad_status }}</div>
                      <div>Honors Program: {{ transcript.honors_program }}</div>
                    </div>
                    <div class="col">
                      <div>Number Courses: {{ transcript.num_courses }}</div>
                      <div>Scholarships: {{ transcript.scholarship_type }}</div>
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
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

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
