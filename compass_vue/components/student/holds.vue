<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2" class="text-danger"
        >Registration Holds</axdd-card-heading
      >
    </template>
    <template #body>
      <ul>
        <li>{{ person.student.registration_hold_ind }}</li>
        <li>
          Office Hold Name: {{ person.student.hold_office_name_combined }}
        </li>
        <li>Hold Reason: {{ person.student.hold_reason_desc_combined }}</li>
      </ul>
    </template>
  </axdd-card>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {},
};
</script>
