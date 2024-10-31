<template>
  <BCard
    class="bg-body-tertiary rounded-3 d-flex flex-fill small"
    border-variant="0"
    body-class="d-flex flex-column"
  >
    <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-3">Status</div>
    <div class="flex-fill">
      <ul class="list-unstyled">
        <li>
          <KeyValue
            v-if="person.student.registration_hold_ind"
            class="text-danger"
          >
            <template #key>Holds</template>
            <template #value>Yes</template>
          </KeyValue>
        </li>
        <li>
          <KeyValue>
            <template #key>Class standing</template>
            <template #value>{{ person.student.class_desc }}</template>
          </KeyValue>
        </li>
        <li>
          <KeyValue>
            <template #key>Campus</template>
            <template #value>{{ person.student.campus_desc }}</template>
          </KeyValue>
        </li>
      </ul>
    </div>
    <div>
      <KeyValue>
        <template #key
          ><span class="fw-bold">Grade Point Average (GPA)</span></template
        >
        <template #value>{{ person.student.cumulative_gpa }}</template>
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
