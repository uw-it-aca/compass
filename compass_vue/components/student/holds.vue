<template>
  <axdd-card v-if="person.student.registration_hold_ind">
    <template #heading>
      <axdd-card-heading :level="2" class="text-danger"
        >Registration Holds</axdd-card-heading
      >
    </template>
    <template #body>
      <ul class="list-unstyled mb-0">
        <li class="mb-1">
          <div class="d-flex">
            <i class="bi bi-exclamation-triangle-fill text-gray me-3"></i>
            <div class="flex-fill">
              <strong>{{ person.student.hold_office_name_combined }}</strong
              ><span class="ms-2 small text-muted">{{
                person.student.hold_reason_desc_combined
              }}</span>
            </div>
          </div>
        </li>
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
