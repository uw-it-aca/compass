<template>
  <div class="row mt-4">
    <div class="col-xl-9">
      <StudentTranscript :person="person"></StudentTranscript>
    </div>
    <div class="col-xl-3">
      <StudentTranscriptCredits :person="person"></StudentTranscriptCredits>
    </div>
  </div>
</template>

<script>
import StudentTranscript from "./transcript.vue";
import StudentTranscriptCredits from "./transcript-credits.vue";

export default {
  components: {
    StudentTranscript,
    StudentTranscriptCredits,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>
