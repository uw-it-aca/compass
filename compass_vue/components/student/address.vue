<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Address</axdd-card-heading>
    </template>
    <template #body>
      <div class="mb-4">
        <p class="small text-uppercase text-muted mb-2">Local Address</p>
        <address>
          {{ person.student.local_addr_line1 }},
          {{ person.student.local_addr_line2 }},<br />
          {{ person.student.local_addr_city }},
          {{ person.student.local_addr_state }}
          {{ person.student.local_addr_5digit_zip }}<br />
          {{ person.student.local_addr_country }}
        </address>
      </div>
      <div class="mb-4">
        <p class="small text-uppercase text-muted mb-2">Permanent Address</p>
        <address>
          {{ person.student.perm_addr_line1 }},
          {{ person.student.perm_addr_line2 }}<br />
          {{ person.student.perm_addr_city }},
          {{ person.student.perm_addr_state }}
          {{ person.student.perm_addr_5digit_zip }}<br />
          {{ person.student.perm_addr_country }}
        </address>
      </div>
      <div>
        <p class="small text-uppercase text-muted mb-2">
          Parent/Guardian Address
        </p>
        <address>
          {{ person.student.parent_addr_line1 }},
          {{ person.student.parent_addr_line2 }}<br />
          {{ person.student.parent_addr_city }},
          {{ person.student.parent_addr_state }}
          {{ person.student.parent_addr_5digit_zip }}<br />
          {{ person.student.parent_addr_country }}
        </address>
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
