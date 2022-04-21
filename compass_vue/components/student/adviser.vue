<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Adviser</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled">
        <li class="fw-bold">John Average</li>
        <li>he/him</li>
        <li>Email</li>
        <li>Phone</li>
        <li class="border-top mt-2 pt-2">Dept Name: OMAD</li>
        <li>Campus location: MGH 123</li>
        <li>
          <a href="#" class="small">Edit adviser (ADMIN)</a>
        </li>
      </ul>

      <div class="border border-danger">
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
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
};
</script>
