<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Majors</axdd-card-heading>
    </template>
    <template #body>
      <ul>
        <li v-for="(major, index) in person.student.majors" :key="index">
          {{ major.major_name }}
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
  data() {
    return {};
  },
};
</script>
