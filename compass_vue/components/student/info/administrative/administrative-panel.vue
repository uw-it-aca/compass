<template>
  <div class="row mt-4">
    <div class="col-xl-9">
      <AffiliationAddEdit :person="person"></AffiliationAddEdit>
    </div>
    <div class="col-xl-3">
      <StudentEligibility :person="person"></StudentEligibility>
    </div>
  </div>
</template>

<script>
import AffiliationAddEdit from "./affiliation.vue";
import StudentEligibility from "./eligibility.vue";

export default {
  components: {
    AffiliationAddEdit,
    StudentEligibility,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>
