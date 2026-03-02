<template>
  <BCard
    class="bg-body-tertiary rounded-3 d-flex flex-fill small"
    border-variant="0"
  >
    <div class="text-uppercase text-body-secondary fs-8 fw-bold mb-3">Degrees</div>

    <div>
      <KeyValue
        v-for="(degree, index) in person.student.degrees"
        :key="index"
        variant="address"
      >
        <template #key
          ><span class="text-wrap">
            {{ degree.degree_desc }}
          </span></template
        >
        <template #value>
          <p v-if="graduationApplicationTerm" class="small">
            {{ graduationApplicationTerm }} ({{ degree.degree_status_desc }})
          </p>
          <p v-else class="small">{{ degree.degree_status_desc }}</p>
        </template>
      </KeyValue>
    </div>
  </BCard>
</template>

<script>
import KeyValue from "@/components/_common/key-value.vue";
import { BCard } from "bootstrap-vue-next";

export default {
  components: { BCard, KeyValue },
  props: {
    person: {
type: Object,:q
      required: true,
    },
  },
  setup() {
    return {};
  },
  data() {
    return {};
  },
  computed: {
    graduationApplicationTerm() {
      return this.person.student.applied_to_graduate_yr_qtr_desc;
    },
  },
  created() {},
  methods: {},
};
</script>
