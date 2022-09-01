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
        <li>Transfer Credits: xxx</li>
        <li>Total Credits Earned: 173.0</li>
      </ul>
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
