<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Address</axdd-card-heading>
    </template>
    <template #body>
      <ul class="list-unstyled m-0">
        <li class="mt-2">
          Perm Address:<br />
          {{ person.student.perm_addr_line1 }},
          {{ person.student.perm_addr_line2 }},
          {{ person.student.perm_addr_city }},
          {{ person.student.perm_addr_state }}
          {{ person.student.perm_addr_5digit_zip }},
          {{ person.student.perm_addr_country }}
        </li>
        <li class="mt-2">
          Local Address:<br />
          {{ person.student.local_addr_line1 }},
          {{ person.student.local_addr_line2 }},
          {{ person.student.local_addr_city }},
          {{ person.student.local_addr_state }}
          {{ person.student.local_addr_5digit_zip }},
          {{ person.student.local_addr_country }}
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
};
</script>
