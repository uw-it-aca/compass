<template>
  <axdd-card v-for="(transcript, transIndex) in transcripts" :key="transIndex">
    <template #heading-action>
      <axdd-card-heading v-if="transcript.term" :level="2"
        >{{ transcript.term.quarter }}
        {{ transcript.term.year }}</axdd-card-heading
      >
      <div v-else>no term data</div>
    </template>
    <template #body>
      <div v-if="transcript.registrations" class="table-responsive m-n3">
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
            <tr
              v-for="(registration, index3) in transcript.registrations" :key="index3">
              <td class="ps-3">
                {{ registration.section.curriculum_abbr }}
                {{ registration.section.course_number }}
              </td>
              <td>{{ registration.section.course_title }}</td>
              <td>{{ registration.credits }}</td>
              <td>{{ registration.grade }}</td>
              <td>{{ registration.is_credit }}</td>
            </tr>
            <tr>
              <td colspan="5" class="">
                <ul class="list-unstyled">
                  <li>QTR ATTEMPTED: {{ transcript.qtr_graded_attmp }}</li>
                  <li>QTR Grade Points EARNED: {{ transcript.qtr_grade_points }}</li>
                  <li>Number of Courses: {{ transcript.registrations.length }}</li>
                </ul>
                <ul class="list-unstyled">
                  <li>Class Code: {{ transcript.class_code }}</li>
                  <li>Enrollment Status: {{ transcript.enrollment_status }}</li>
                  <li>Exemption Code: {{ transcript.exemption_code }}</li>
                  <li>Grad status: {{ transcript.grad_status }}</li>
                  <li>Honors Program: {{ transcript.is_honors }}</li>
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
