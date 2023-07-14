<template>
  <div class="row mt-4">
    <div class="col-xl-9">
      <StudentContact :person="person"></StudentContact>
    </div>
    <div class="col-xl-3">
      <StudentVisits :person="person"></StudentVisits>
    </div>
  </div>
</template>

<script>
import StudentContact from "./contact.vue";
import StudentVisits from "./visits.vue";

export default {
  components: {
    StudentContact,
    StudentVisits,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>
