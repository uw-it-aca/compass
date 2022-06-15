<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Special Programs</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled small">
        <li>
          Special Program Code:
          {{ person.student.transcripts[0].special_program }}
        </li>
      </ul>

      <div class="fw-bold">OMAD Programs</div>
      <div class="border border-danger p-1 small">
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            value
            id="defaultCheck1"
          />
          <label class="form-check-label" for="defaultCheck1">CAMP</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            value
            id="defaultCheck2"
          />
          <label class="form-check-label" for="defaultCheck2">TRIO SSS</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            value
            id="defaultCheck4"
          />
          <label class="form-check-label" for="defaultCheck4">Champions</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            value
            id="defaultCheck5"
          />
          <label class="form-check-label" for="defaultCheck5"
            >IC Eligible</label
          >
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            value
            id="defaultCheck3"
          />
          <label class="form-check-label" for="defaultCheck3"
            >Pre-professional</label
          >
        </div>
        <div class="mt-3">
          <button type="button" class="btn btn-outline-dark-beige btn-sm">
            Update programs
          </button>
        </div>
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
  data() {
    return {};
  },
};
</script>
