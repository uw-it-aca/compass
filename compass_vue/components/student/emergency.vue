<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Emergency Contact</axdd-card-heading>
    </template>
    <template #body>
      <div class="mb-4">
        <p class="small text-uppercase text-muted mb-2">Perm Address</p>
        <div>{{ person.student.emergency_name }}, {{ person.student.emergency_phone }}, {{ person.student.emergency_email }}</div>
      </div>
    </template>
  </axdd-card>
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
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
};
</script>
