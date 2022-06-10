<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Academics</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled small">
        <li>
          Enrollment Status:
          <template v-if="person.student.registered_in_quarter">
            Registered
          </template>
          <template v-else> Unregistered </template
          >{{ person.student.enrollment_desc }}
        </li>
        <li>Class standing: {{ person.student.class_desc }}</li>
        <li>Total Credits: {{ person.student.total_credits }}</li>
        <li>Total UW Credits: {{ person.student.total_uw_credits }}</li>
        <li>
          Transfer credits:
          <span class="text-danger">tbd</span>
        </li>
        <li>GPA: {{ person.student.cumulative_gpa }}</li>
        <li class="border-top mt-2 pt-2">Scholarships: <span class="text-danger">tbd</span></li>
        <li>Yearly Honors: <span class="text-danger">tbd</span></li>
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
