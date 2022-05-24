<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Academics</axdd-card-heading>
    </template>
    <template #body>
      <ul>
        <li>
          Accepted:
          <span v-for="(major, index) in person.student.majors" :key="index">
            {{ major.major_name }}
            <span v-if="index + 1 < person.student.majors.length">,</span>
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
