<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Special Programs</axdd-card-heading>
    </template>
    <template #body>
      <p class="small">https://studentdata.washington.edu/sdb-code-manual/student/sdb-special-program-codes/</p>
      <ul>
        <li>Honor's</li>
        <li>Athletics</li>
        <li>EOP</li>
      </ul>
    </template>
  </axdd-card>

  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Programs (compass)</axdd-card-heading>
    </template>
    <template #body>
      <p>OMAD Programs</p>
      <div class="border border-danger">
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
          <label class="form-check-label" for="defaultCheck3">Pre-professional</label>
        </div>
        <div class="text-end">
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
