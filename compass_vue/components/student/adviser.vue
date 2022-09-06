<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Adviser</axdd-card-heading>
    </template>
    <template #body>
      <div v-if="advisers">
        <ul
          v-for="adviser in advisers"
          :key="adviser.id"
          class="list-unstyled mb-0"
        >
          <li class="mb-1 d-flex">
            <i class="bi bi-person-circle text-gray me-3"></i>
            <div class="flex-fill">
              <strong>{{ adviser.display_name }}</strong> ({{
                adviser.uwnetid
              }})<br />{{ adviser.pronouns }}
            </div>
          </li>
          <li class="mb-1">
            <i class="bi bi-envelope-fill text-gray me-3"></i>
            <span>{{ adviser.employee.adviser.advising_email }}</span>
          </li>
          <li class="mb-1">
            <i class="bi bi-telephone text-gray me-3"></i>
            <span>{{ adviser.employee.adviser.advising_phone_number }}</span>
          </li>
          <li class="mb-1">
            <i class="bi bi-building text-gray me-3"></i>
            <span>{{ adviser.employee.adviser.advising_program }}</span>
          </li>
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
