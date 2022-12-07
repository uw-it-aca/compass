<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Affiliations</axdd-card-heading>
    </template>
    <template #body>
      <div>
        <div class="fs-7 text fw-bold text-secondary">Cohort</div>
        <div class="fs-7 text fw-bold text-secondary">Programs</div>
        <div class="fs-7 text fw-bold text-secondary">Affiliations</div>
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
