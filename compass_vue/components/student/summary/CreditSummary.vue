<template>
  <BCard
    class="bg-body-tertiary rounded-3 d-flex flex-fill small"
    border-variant="0"
    body-class="d-flex flex-column"
  >
    <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-3">Credits</div>
    <div class="flex-fill">
      <ul class="list-unstyled">
        <li>
          <KeyValue>
            <template #key>Total Extension Credits</template>
            <template #value>{{
              person.student.total_extension_credits
            }}</template>
          </KeyValue>
        </li>
        <li>
          <KeyValue>
            <template #key>Total Transfer Credits</template>
            <template #value>{{
              person.student.total_transfer_credits
            }}</template>
          </KeyValue>
        </li>
        <li>
          <KeyValue>
            <template #key>Total UW Credits</template>
            <template #value>{{ person.student.total_uw_credits }}</template>
          </KeyValue>
        </li>
      </ul>
    </div>
    <div>
      <KeyValue>
        <template #key><span class="fw-bold">Total Credits</span></template>
        <template #value>{{ person.student.total_credits }}</template>
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
