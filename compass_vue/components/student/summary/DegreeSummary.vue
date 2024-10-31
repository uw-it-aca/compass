<template>
  <BCard
    class="bg-body-tertiary rounded-3 d-flex flex-fill small"
    border-variant="0"
  >
    <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-3">Degrees</div>

    <div>
      <KeyValue
        variant="address"
        v-for="(degree, index) in person.student.degrees"
        :key="index"
      >
        <template #key
          ><span class="text-wrap">
            {{ degree.degree_desc }}
          </span></template
        >
        <template #value>
          <p class="small" v-if="degree.degree_term">
            {{ degree.degree_term.quarter_name }}
            {{ degree.degree_term.year }}
            ({{ degree.degree_status_desc }})
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
      type: Object,
      required: true,
    },
  },
  setup() {
    return {};
  },
  data() {
    return {};
  },
  created() {},
  methods: {},
};
</script>
