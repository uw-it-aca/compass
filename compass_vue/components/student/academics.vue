<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Academics</axdd-card-heading>
    </template>
    <template #body>
      <ul>
        <li>
          Registered:
          <template v-if="person.student.registered_in_quarter">
            <b>yes</b>/no
          </template>
          <template v-else>
            yes/
            <b>no</b>
          </template>
        </li>
        <li>Enrollment Status: {{ person.student.enrollment_desc }}</li>
        <li>Class standing: {{ person.student.class_desc }}</li>
        <li>Total Credits: {{ person.student.total_credits }}</li>
        <li>Total UW Credits: {{ person.student.total_uw_credits }}</li>
        <li>
          Transfer student:
          <b>yes</b>/no
        </li>
        <li>GPA: {{ person.student.cumulative_gpa }}</li>
      </ul>
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
  data() {
    return {};
  },
};
</script>
