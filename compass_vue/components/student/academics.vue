<template>
  <div class="row mb-4">
    <h2 class="h6 m-0 fw-bold mb-4">Academic Summary</h2>

    <div
      class="col-xl-3 d-flex flex-column"
      :class="[mq.lgMinus ? 'mb-4' : '']"
    >
      <StatusSummary :person="person"></StatusSummary>
    </div>
    <div
      class="col-xl-3 d-flex flex-column"
      :class="[mq.lgMinus ? 'mb-4' : '']"
    >
      <DegreeSummary
        v-if="person.student.degrees && person.student.degrees.length > 0"
        :person="person"
      ></DegreeSummary>
      <MajorSummary
        v-if="person.student.degrees && person.student.degrees.length == 0"
        :person="person"
      ></MajorSummary>
    </div>
    <div
      class="col-xl-3 d-flex flex-column"
      :class="[mq.lgMinus ? 'mb-4' : '']"
    >
      <AffiliationSummary :person="person"></AffiliationSummary>
    </div>
    <div class="col-xl-3 d-flex flex-column">
      <CreditSummary :person="person"></CreditSummary>
    </div>
  </div>
</template>

<script>
import AffiliationSummary from "@/components/student/summary/AffiliationSummary.vue";
import StatusSummary from "@/components/student/summary/StatusSummary.vue";
import CreditSummary from "@/components/student/summary/CreditSummary.vue";
import DegreeSummary from "@/components/student/summary/DegreeSummary.vue";
import MajorSummary from "@/components/student/summary/MajorSummary.vue";

import { translateTrueFalse } from "@/utils/translations";

export default {
  name: "StudentAcademics",
  components: {
    AffiliationSummary,
    StatusSummary,
    CreditSummary,
    DegreeSummary,
    MajorSummary,
  },
  inject: ["mq"],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      translateTrueFalse,
    };
  },
  data() {
    return {
      testObj: {},
    };
  },
  created() {},
  methods: {},
};
</script>
