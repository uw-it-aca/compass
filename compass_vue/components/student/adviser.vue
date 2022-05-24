<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Adviser</axdd-card-heading>
    </template>
    <template #body>
      <ul v-if="person.employee.adviser" class="list-unstyled">
        <li class="fw-bold">{{person.display_name}}</li>
        <li>he/him</li>
        <li>Email: {{person.employee.adviser.advising_email}}</li>
        <li>Phone: {{person.employee.adviser.advising_phone_number}}</li>
        <li class="border-top mt-2 pt-2">Dept Name: {{person.employee.adviser.advising_program}}</li>
        <li>Campus location: MGH 123</li>
        <li>
          <a href="#" class="small">Edit adviser (ADMIN)</a>
        </li>
      </ul>

      <div v-else class="border border-danger">
        <ul class="list-unstyled text-muted">
          <li>
            <p>This student does not have an assigned adviser.</p>
          </li>
          <li>
            <select
              class="form-select form-select-sm mb-2"
              aria-label=".form-select-sm example"
            >
              <option selected>Select adviser</option>
              <option value="1">Bob</option>
              <option value="2">Tim</option>
              <option value="3">Joe</option>
            </select>
          </li>
          <li class="text-end">
            <button type="button" class="btn btn-outline-dark-beige btn-sm">
              Update adviser
            </button>
          </li>
        </ul>
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
