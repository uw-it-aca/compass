<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Programs</axdd-card-heading>
    </template>
    <template #body>
      <AddCustomField :field-type="'program'"></AddCustomField>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";
import AddCustomField from "../add-custom-field.vue";

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
    AddCustomField,
  },
  data() {
    return {};
  },
};
</script>
