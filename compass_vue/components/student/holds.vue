<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Holds</axdd-card-heading>
    </template>
    <template #body>
      <div>
        <div class="fw-bold text-danger">Registration Hold:</div>
        <ul>
          <li>
            Office Hold Name: {{ person.student.hold_office_name_combined }}
          </li>
          <li>Hold Reason: {{ person.student.hold_reason_desc_combined }}</li>
        </ul>
      </div>
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
