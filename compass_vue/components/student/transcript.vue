<template>
  <div v-if="isLoading">
    <span>Loading...</span>
  </div>
  <template v-else-if="transcripts.length">
    <BCard
      v-for="(transcript, transIndex) in transcripts"
      :key="transIndex"
      class="shadow-sm rounded-3 mb-3"
      header-class="p-3 d-flex align-items-center justify-content-between"
      header-bg-variant="transparent"
      body-class="p-0"
    >
      <template #header>
        <template v-if="transcript.class_schedule">
          <div class="fs-6 fw-bold">
            {{ transcript.class_schedule.term.quarter }}
            {{ transcript.class_schedule.term.year }}
          </div>
        </template>
        <div v-else>no term data</div>
      </template>

      <div v-if="transcript.class_schedule" class="table-responsive m-0">
        <table class="table m-0">
          <thead class="text-muted small">
            <tr>
              <th class="ps-3 bg-body-tertiary">Course</th>
              <th class="bg-body-tertiary">Title</th>
              <th class="bg-body-tertiary">Credits</th>
              <th class="bg-body-tertiary">Grade</th>
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
              <td colspan="4" class="ps-3">
                <div class="d-flex justify-content-between">
                  <ul class="list-unstyled w-50 m-0">
                    <li>
                      Credits Attempted:
                      {{ formatCredits(transcript.cmp_qtr_total_attempted) }}
                    </li>
                    <li>
                      Graded Attempted:
                      {{ formatCredits(transcript.cmp_qtr_graded_attempted) }}
                    </li>
                    <li>
                      Graded Earned:
                      {{ formatCredits(transcript.cmp_qtr_graded_earned) }}
                    </li>
                    <li>
                      Grade Points:
                      {{ transcript.cmp_qtr_grade_points }}
                    </li>
                    <li>
                      GPA: <strong>{{ transcript.cmp_qtr_gpa }}</strong>
                    </li>
                  </ul>

                  <ul class="list-unstyled w-50 m-0">
                    <li>
                      Cumulative Credits Attempted:
                      {{ formatCredits(transcript.cmp_cum_total_attempted) }}
                    </li>
                    <li>
                      Cumulative Graded Attempted:
                      {{ formatCredits(transcript.cmp_cum_graded_attempted) }}
                    </li>
                    <li>
                      Cumulative UW Earned:
                      {{ formatCredits(transcript.cmp_cum_uw_earned) }}
                    </li>
                    <li>
                      Cumulative Total Earned:
                      {{ formatCredits(transcript.cmp_cum_total_earned) }}
                    </li>
                    <li>
                      Cumulative Grade Points:
                      {{ transcript.cmp_cum_grade_points }}
                    </li>
                    <li>
                      Cumulative GPA:
                      <strong>{{ transcript.cmp_cum_gpa }}</strong>
                    </li>
                  </ul>

                  <ul class="d-none list-unstyled">
                    <li>Class Code: {{ transcript.special_program }}</li>
                    <li>Enrollment Status: {{ transcript.enroll_status }}</li>
                    <li>Exemption Code: {{ transcript.exemption_code }}</li>
                    <li>Grad status: {{ transcript.grad_status }}</li>
                    <li>Honors Program: {{ transcript.honors_program }}</li>
                    <li>Scholarship Code: {{ transcript.scholarship_type }}</li>
                    <li>
                      Special Program Code: {{ transcript.special_program }}
                    </li>
                    <li>Veteran: {{ transcript.veteran }}</li>
                    <li>Veteran Benefit: {{ transcript.veteran_benefit }}</li>
                  </ul>
                </div>
                <div v-if="academicStanding(transcript.scholarship_type)">
                  Academic Standing: {{ academicStanding(transcript.scholarship_type) }}
                </div>
                <div>{{ transcript.qtr_comment }}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="p-3">no transcript for this term</div>
    </BCard>
  </template>
  <div v-else class="p-3">no academic history available for this student.</div>
</template>

<script>
import { useStudentStore } from "@/stores/student";
import { BCard } from "bootstrap-vue-next";

export default {
  name: "StudentTranscript",
  components: { BCard },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const storeStudent = useStudentStore();
    return { storeStudent };
  },
  data() {
    return {
      transcripts: [],
      isLoading: false,
    };
  },
  created() {
    this.loadStudentTranscripts();
  },
  methods: {
    formatCredits: function (credits) {
      return credits !== null ? credits.toFixed(1) : "0.0";
    },
    academicStanding: function (scholarship_type) {
        return scholarship_type == 1 ? "Dean's List"
            : scholarship_type == 3 ? "Warning"
            : scholarship_type == 4 ? "Alert"
            : scholarship_type == 5 ? "Drop"
            : scholarship_type == 6 ? "Reinstate"
            : null;

    },
    loadStudentTranscripts: function () {
      let uwregid = this.person.uwregid;
      this.isLoading = true;
      this.storeStudent.fetchStudentTranscripts(uwregid)
        .then(() => {
          this.transcripts = this.storeStudent.transcripts[uwregid].data;
        })
        .finally(() => {
          this.isLoading = false;
        });

    },
  },
};
</script>
