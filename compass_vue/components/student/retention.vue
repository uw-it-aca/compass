<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Retention</axdd-card-heading>
    </template>
    <template #body>
      <ul>
        <li>
          Priority:
          <span class="fw-bold">{{ student.retention.priority }}</span>
        </li>
        <li>Sign-ins: {{ student.retention.sign_in }}</li>
        <li>Activity: {{ student.retention.activity }}</li>
        <li>Assignments: {{ student.retention.assignment }}</li>
        <li>Grades: {{ student.retention.grade }}</li>
      </ul>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from 'axdd-components';

export default {
  props: {
    student: {
      type: Object,
      required: true,
    },
  },
  components: {
    'axdd-card': Card,
    'axdd-card-heading': CardHeading,
  },
  data() {
    return {};
  },
};
</script>
