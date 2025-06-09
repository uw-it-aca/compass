<template>
  <BCard
    class="shadow-sm rounded-3"
    header-class="p-3 d-flex align-items-center justify-content-between"
    header-bg-variant="transparent"
    footer-bg-variant="transparent"
  >
    <template #header>
      <div class="fs-6 fw-bold">Credit summary</div>
    </template>

    <ul class="list-unstyled">
      <li>
        <div class="d-flex justify-content-between">
          <span>UW Credits Attempted:</span>
          <span v-if="latestTranscript">
            {{ latestTranscript.cmp_cum_total_attempted.toFixed(1) }}
          </span>
        </div>
      </li>
      <li>
        <div class="d-flex justify-content-between">
          <span>UW Graded Attempted:</span>
          <span v-if="latestTranscript">
            {{ latestTranscript.cmp_cum_graded_attempted.toFixed(1) }}
          </span>
        </div>
      </li>
      <li>
        <div class="d-flex justify-content-between">
          <span>UW Graded Earned:</span>
          <span v-if="latestTranscript">
            {{ latestTranscript.cmp_cum_graded_earned.toFixed(1) }}
          </span>
        </div>
      </li>
      <li>
        <div class="d-flex justify-content-between">
          <span>UW Grade Points:</span>
          <span v-if="latestTranscript">
            {{ latestTranscript.cmp_cum_grade_points }}
          </span>
        </div>
      </li>
      <li>
        <div class="d-flex justify-content-between">
          <span>UW GPA:</span>
          <span v-if="latestTranscript" class="fw-bold">
            {{ latestTranscript.cmp_cum_gpa }}
          </span>
        </div>
      </li>
    </ul>
    <ul class="list-unstyled m-0">
      <li>
        <div class="d-flex justify-content-between">
          <span>UW Credits Earned:</span>
          <span>{{ person.student.total_uw_credits }}</span>
        </div>
      </li>
      <li>
        <div class="d-flex justify-content-between">
          <span>Extension Credits:</span>
          <span>{{ person.student.total_extension_credits }}</span>
        </div>
      </li>
      <li>
        <div class="d-flex justify-content-between">
          <span>Transfer Credits:</span>
          <span>{{ person.student.total_transfer_credits }}</span>
        </div>
      </li>
      <li><hr /></li>
      <li>
        <div class="d-flex justify-content-between">
          <span>Credits Earned</span>
          <span>{{ person.student.total_credits }}</span>
        </div>
      </li>
    </ul>
  </BCard>
</template>

<script>
import { useStudentStore } from "@/stores/student";
import { BCard } from "bootstrap-vue-next";

export default {
  name: "StudentTranscriptCredits",
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
      latestTranscript: null,
    };
  },
  mounted() {
    this.loadLatestTranscript();
  },
  methods: {
    loadLatestTranscript: function () {
      let uwregid = this.person.uwregid;
      this.storeStudent.fetchStudentTranscripts(uwregid)
        .then(() => {
          if (this.storeStudent.transcripts[uwregid].data.length) {
            this.latestTranscript = this.storeStudent.transcripts[uwregid].data[0];
          }
        });
    },
  },
};
</script>
