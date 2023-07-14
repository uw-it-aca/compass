<template>
  <div class="row mt-4">
    <div class="col-xl-12">
      <StudentAcademics :person="person"></StudentAcademics>
    </div>
    <div class="col-xl-9">
      <StudentSchedule :person="person"></StudentSchedule>
    </div>
    <div class="col-xl-3">
      <StudentHolds :person="person"></StudentHolds>
      <StudentAdviser :advisers="person.student.advisers"></StudentAdviser>
    </div>
  </div>
</template>

<script>
import StudentAcademics from "./academics.vue";
import StudentSchedule from "./schedule.vue";
import StudentHolds from "./holds.vue";
import StudentAdviser from "./adviser.vue";

export default {
  components: {
    StudentAcademics,
    StudentSchedule,
    StudentHolds,
    StudentAdviser,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>
