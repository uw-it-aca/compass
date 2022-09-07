<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Credit summary</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled">
        <li>UW Credits Attempted: xxx</li>
        <li>UW Credits Earned: xxx</li>
        <li>UW Graded Attempted: xxx</li>
        <li>UW Graded Earned: xxx</li>
        <li>UW Graded Points: xxx</li>
        <li>UW Grade Point Average: xxx</li>
        <li>Extension Credits: xxx</li>
        <li>Transfer Credits: {{ person.student.total_transfer_credits }}</li>
        <li>Total UW Credits Earned: {{ person.student.total_uw_credits }}</li>
      </ul>
      <ul class="list-unstyled">
        <li>
          Total Deductible Credits:
          {{ person.student.total_deductible_credits }}
        </li>
        <li>
          Total Extension Credits:
          {{ person.student.total_extension_credits }}
        </li>
        <li>
          Total Non-Graded Credits:
          {{ person.student.total_non_graded_credits }}
        </li>
        <li>
          Total Registered Credits:
          {{ person.student.total_registered_credits }}
        </li>
        <li>
          Total Transfer Credits:
          {{ person.student.total_transfer_credits }}
        </li>
        <li><hr /></li>
        <li>
          <div class="d-flex justify-content-between">
            <span>Total Credits</span>
            <span>{{ person.student.total_credits }}</span>
          </div>
        </li>
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
};
</script>
