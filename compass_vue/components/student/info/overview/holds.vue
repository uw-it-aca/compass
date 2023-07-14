<template>
  <axdd-card v-if="person.student.registration_hold_ind">
    <template #heading>
      <axdd-card-heading :level="2" class="text-danger"
        >Holds</axdd-card-heading
      >
    </template>
    <template #body>
      <ul class="list-unstyled mb-0">
        <li
          v-for="(hold, index) in person.student.holds"
          :key="index"
          class="mb-1"
        >
          <div class="d-flex">
            <i class="bi bi-exclamation-triangle-fill text-gray me-3"></i>
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
    </template>
  </axdd-card>
</template>

<script>
import { formatDate } from "../../../../utils/dates";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
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
