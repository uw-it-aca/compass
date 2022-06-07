<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Adviser</axdd-card-heading>
    </template>
    <template #body>
      <p class="small">current user: {{ userNetid }}, {{ userRole }}</p>
      <div class="border p-1 mb-2 small">
        <p class="text-muted">if has advisers</p>
        <ul v-for="adviser in advisers" :key="adviser.id" class="list-unstyled">
          <li>Display name: {{ adviser.display_name }}</li>
          <li>Pronouns: {{ adviser.pronouns }}</li>
          <li>Netid: <span class="text-danger">netid</span></li>
          <li>Email: {{ adviser.employee.adviser.advising_email }}</li>
          <li>Phone: {{ adviser.employee.adviser.advising_phone_number }}</li>
          <li>Dept Name: {{ adviser.employee.adviser.advising_program }}</li>
          <li>Campus location: <span class="text-danger">MGH 123</span></li>
        </ul>
      </div>

      <div class="border border-danger p-1 mb-5 small">
        <p class="text-danger">else (empty)</p>
        <p>This student does not have an assigned adviser.</p>
        <button type="button" class="btn btn-outline-dark-beige btn-sm">
          Add to your caseload
        </button>
        <div class="small text-danger">
          This should write back to SWS. Student must either be EOP1 or EOP3.
        </div>
      </div>

      <div class="border border-danger p-1 small">
        <p class="text-danger">if (role == manager)</p>
        <p>Assign a new adviser for this student!</p>
        <select
          class="form-select form-select-sm mb-2"
          aria-label=".form-select-sm example"
        >
          <option selected>Select group adviser</option>
          <option value="1">Bob</option>
          <option value="2">Tim</option>
          <option value="3">Joe</option>
          <option value="4">Jay</option>
        </select>

        <button type="button" class="btn btn-outline-dark-beige btn-sm">
          Update adviser
        </button>
        <div class="small text-danger">
          This should write back to SWS. Student must either be EOP1 or EOP3.
        </div>
      </div>
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
