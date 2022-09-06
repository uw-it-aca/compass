<template>
  <div class="d-flex">

    <div class="flex-fill">
      <div class="text-nowrap">
        <span class="me-2">
          <router-link :to="{ path: '/student/' + person.uwnetid }"
            >{{ person.display_name }} ({{ person.uwnetid }})</router-link
          >
        </span>
        <span
          v-if="person.student.gender === 'M'"
          class="badge rounded-pill border border-muted text-dark"
          >M</span
        >
        <span
          v-if="person.student.gender === 'F'"
          class="badge rounded-pill border border-muted text-dark"
          >F</span
        >
      </div>
      <div class="text-secondary">
        {{ person.student.student_number }}, {{ person.student.class_desc }},
        <template v-if="person.student.registered_in_quarter">
          Registered
        </template>
        <template v-else> Unregistered </template>
      </div>
    </div>
  </div>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
  data() {
    return {};
  },
};
</script>
