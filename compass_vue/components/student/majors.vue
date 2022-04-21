<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Academics</axdd-card-heading>
    </template>
    <template #body>
      <ul>
        <li>
          Accepted:
          <span v-for="(major, index) in student.major" :key="index">
            {{ major.major_full_name }}
            <span v-if="index + 1 < student.major.length">,</span>
          </span>
        </li>
      </ul>
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
