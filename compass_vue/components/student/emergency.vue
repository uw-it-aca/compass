<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Emergency Contact</axdd-card-heading>
    </template>
    <template #body>
      <div>
        <p class="small text-uppercase text-muted mb-2">Contact</p>
        <ul class="list-unstyled mb-0">
          <li>
            <div class="d-flex">
              <i class="bi bi-person-circle text-gray me-3"></i>
              <div class="flex-fill">
                {{ person.student.emergency_name }}
              </div>
            </div>
          </li>
          <li>
            <div class="d-flex">
              <i class="bi bi-envelope-fill text-gray me-3"></i>
              <div class="flex-fill">
                {{ person.student.emergency_email }}
              </div>
            </div>
           </li>
           <li>
            <div class="d-flex">
              <i class="bi bi-telephone text-gray me-3"></i>
              <div class="flex-fill">
                {{ person.student.emergency_phone }}
              </div>
            </div>
          </li>
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
