<template>
  <BCard
    v-if="person.student.registration_hold_ind"
    class="shadow-sm rounded-3 mb-4"
    header-class="p-3"
    header-bg-variant="transparent"
  >
    <template #header><div class="fs-6 fw-bold">Holds</div></template>
    <ul class="list-unstyled mb-0">
      <li
        v-for="(hold, index) in person.student.holds"
        :key="index"
        class="mb-1"
      >
        <div class="d-flex">
          <i
            class="bi bi-exclamation-triangle-fill text-body-tertiary me-3"
          ></i>
          <div class="flex-fill">
            <strong>{{ hold.hold_office_desc }}</strong>
            <div>{{ hold.hold_reason }}</div>
            <div class="small text-muted">
              {{ formatDate(hold.hold_dt, "LL") }}
            </div>
            <div class="small text-muted">{{ hold.hold_type_desc }}</div>
          </div>
        </div>
      </li>
    </ul>
  </BCard>
</template>

<script>
import { formatDate } from "@/utils/dates";
import { BCard } from "bootstrap-vue-next";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: { BCard },
  setup() {
    return {
      formatDate,
    };
  },
  data() {
    return {};
  },
};
</script>
