<template>
  <template v-if="transcripts">
    <axdd-card
      v-for="(transcript, transIndex) in transcripts"
      :key="transIndex"
    >
      <template #heading-action>
        <template v-if="transcript.class_schedule">
          <axdd-card-heading :level="2">
            {{ transcript.class_schedule.term.quarter }}
            {{ transcript.class_schedule.term.year }}
          </axdd-card-heading>
        </template>
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
              </tr>
            </thead>
            <tbody>
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
              </tr>
              <tr>
                <td colspan="4">
                  <div class="d-flex justify-content-between">
                    <ul class="list-unstyled w-50">
                      <li>QTR ATTEMPTED: {{ transcript.qtr_graded_attmp }}</li>
                      <li>QTR EARNED: xx</li>
                      <li>
                        QTR GRADE POINTS: {{ transcript.qtr_grade_points }}
                      </li>
                      <li>
                        QTR GPA (calculated):
                        <strong>{{
                          (
                            transcript.qtr_grade_points /
                            transcript.qtr_graded_attmp
                          ).toFixed(2)
                        }}</strong>
                      </li>
                      <li>QTR GRADED AT: xx</li>
                    </ul>

                    <ul class="list-unstyled w-50">
                      <li>CUM ATTEMPTED: xx</li>
                      <li>UW EARNED: xx</li>
                      <li>TTL EARNED: xx</li>
                      <li>CUM GRADED AT: xx</li>
                      <li>CUM GRADE PTS: xx</li>
                      <li>CUM GPA: xx</li>
                    </ul>

                    <ul class="d-none list-unstyled">
                      <li>Class Code: {{ transcript.special_program }}</li>
                      <li>Enrollment Status: {{ transcript.enroll_status }}</li>
                      <li>Exemption Code: {{ transcript.exemption_code }}</li>
                      <li>Grad status: {{ transcript.grad_status }}</li>
                      <li>Honors Program: {{ transcript.honors_program }}</li>
                      <li>
                        Scholarship Code: {{ transcript.scholarship_type }}
                      </li>
                      <li>
                        Special Program Code: {{ transcript.special_program }}
                      </li>
                      <li>Veteran: {{ transcript.veteran }}</li>
                      <li>Veteran Benefit: {{ transcript.veteran_benefit }}</li>
                    </ul>
                  </div>
                  <div v-if="transcript.scholarship_type == 3">
                    SCHOLARSHIP STATUS: PROBATION
                  </div>
                  <div v-else-if="transcript.scholarship_type == 4">
                    SCHOLARSHIP STATUS: WARNING
                  </div>
                  <div v-else-if="transcript.scholarship_type == 1">
                    SCHOLARSHIP STATUS: DEAN'S LIST
                  </div>

                  <div>{{ transcript.qtr_comment }}</div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else><p>no transcript for this term</p></div>
      </template>
    </axdd-card>
  </template>
  <template v-else>
    <p>no transcripts yet</p>
  </template>
</template>

<script>
import { useStudentStore } from "@/stores/student";

export default {
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
  setup() {
    const storeStudent = useStudentStore();
    return { storeStudent };
  },
  created() {
    this.loadStudentTranscripts();
  },
  methods: {
    loadStudentTranscripts: function () {
      this.storeStudent
        .fetchStudentTranscripts(this.person.uwregid)
        .then(() => {
          this.transcripts =
            this.storeStudent.studentData[this.person.uwregid].data;
        });
    },
  },
};
</script>
