<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Adviser</axdd-card-heading>
    </template>
    <template #body>
      <div v-if="advisers" class="mb-2">
        <ul v-for="adviser in advisers" :key="adviser.id" class="list-unstyled">
          <li>Display name: {{ adviser.display_name }}</li>
          <li>Pronouns: {{ adviser.pronouns }}</li>
          <li>Netid: {{ adviser.uwnetid }}</li>
          <li>Email: {{ adviser.employee.adviser.advising_email }}</li>
          <li>Phone: {{ adviser.employee.adviser.advising_phone_number }}</li>
          <li>Dept Name: {{ adviser.employee.adviser.advising_program }}</li>
          <li>Campus location: <span class="text-danger">MGH 123</span></li>
        </ul>
      </div>
      <div v-else>No adviser assigned to this student.</div>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

export default {
  props: {
    advisers: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      userNetid: document.body.getAttribute("data-user-netid"),
      userRole: document.body.getAttribute("data-user-role"),
    };
  },
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
};
</script>
