<template>
  <BCard
    class="bg-body-tertiary rounded-3 d-flex flex-fill small"
    border-variant="0"
  >
    <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-3">Majors</div>

    <!-- current majors -->
    <div v-if="person.student.majors.length > 0">
      <KeyValue variant="address">
        <template #key>Current Majors</template>
        <template #value>
          <ul class="list-unstyled">
            <li v-for="(major, index) in person.student.majors" :key="index">
              {{ major.major_abbr_code }}, {{ major.major_name }}
            </li>
          </ul>
        </template>
      </KeyValue>
    </div>
    <!-- pending majors -->
    <div v-else>
      <KeyValue variant="address">
        <template #key>Pending Majors</template>
        <template #value>
          <ul class="list-unstyled">
            <li
              v-for="(pending, index) in person.student.pending_majors"
              :key="index"
            >
              {{ pending.major_abbr_code }}, {{ pending.major_name }}
            </li>
          </ul>
        </template>
      </KeyValue>
    </div>
    <!-- requested majors -->
    <div>
      <KeyValue variant="address">
        <template #key>Requested Majors</template>
        <template #value>
          <ul class="list-unstyled">
            <li
              v-for="(requested, index) in person.student.requested_majors"
              :key="index"
            >
              {{ requested }}
            </li>
          </ul>
        </template>
      </KeyValue>
    </div>
    <!-- intended majors -->
    <div>
      <KeyValue variant="address">
        <template #key>Intended Majors</template>
        <template #value>
          <ul class="list-unstyled">
            <li
              v-for="(intended, index) in person.student.intended_majors"
              :key="index"
            >
              {{ intended }}
            </li>
          </ul>
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
