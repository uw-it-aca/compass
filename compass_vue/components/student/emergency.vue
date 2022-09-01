<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Emergency Contact</axdd-card-heading>
    </template>
    <template #body>
      <p>Emergency contanct info</p>
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
