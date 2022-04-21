<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Programs</axdd-card-heading>
    </template>
    <template #body>
      <p>UW Programs (from EDW?)</p>
      <ul>
        <li>Honor's</li>
        <li>Dean's List</li>
        <li>Athletics</li>
        <li>EOP</li>
      </ul>

      <hr />

      <p>OMAD Programs (if EOP yes)</p>
      <ul>
        <li>Pre-professional: yes/no</li>
        <li>IC Eligible: yes/no</li>
        <li>
          <template v-if="student.special_program_code">
            <b>yes</b>/no
          </template>
          <template v-else>CAMP, TRIO SSS, Champions</template>
        </li>
      </ul>
      <p>
        <a href="#" class="small">Edit Programs (ADMIN)</a>
      </p>
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
          <label class="form-check-label" for="defaultCheck2">TRIO</label>
        </div>
        <div class="form-check">
          <input
            class="form-check-input"
            type="checkbox"
            value
            id="defaultCheck3"
          />
          <label class="form-check-label" for="defaultCheck3">SSS</label>
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
    student: {
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
