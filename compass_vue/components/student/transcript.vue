<template>
  <axdd-card v-for="(transcript, transIndex) in transcripts" :key="transIndex">
    <template #heading-action>
      <axdd-card-heading v-if="transcript.class_schedule" :level="2"
        >{{ transcript.class_schedule.term.quarter }}
        {{ transcript.class_schedule.term.year }}</axdd-card-heading
      >
      <div v-else>no term data</div>
    </template>
    <template #body>
      <div v-if="transcript.class_schedule" class="table-responsive m-n3">
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
          <tbody>
            {{
              transcript
            }}
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
              <td colspan="5" class="">
                <ul class="list-unstyled">
                  <li>QTR ATTEMPTED: {{ transcript.qtr_graded_attmp }}</li>
                  <li>QTR EARNED: {{ transcript.qtr_grade_points }}</li>
                  <li>Number of Courses: {{ transcript.num_courses }}</li>
                </ul>
                <ul class="list-unstyled">
                  <li>Class Code: {{ transcript.special_program }}</li>
                  <li>Enrollment Status: {{ transcript.enroll_status }}</li>
                  <li>Exemption Code: {{ transcript.exemption_code }}</li>
                  <li>Grad status: {{ transcript.grad_status }}</li>
                  <li>Honors Program: {{ transcript.honors_program }}</li>
                  <li>Scholarships: {{ transcript.scholarship_type }}</li>
                  <li>
                    Special Program Code: {{ transcript.special_program }}
                  </li>
                  <li>Veteran: {{ transcript.veteran }}</li>
                  <li>Veteran Benefit: {{ transcript.veteran_benefit }}</li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else><p>no transcript for this term</p></div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
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
