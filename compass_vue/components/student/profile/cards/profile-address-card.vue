<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Address
  </div>
  <ul class="list-unstyled m-0 small">
    <li>
      <KeyValue variant="address">
        <template #key>Local Address</template>
        <template #value>
          <address>
            {{ person.student.local_addr_line1 }}
            {{ person.student.local_addr_line2 }},
            {{ person.student.local_addr_city }},
            {{ person.student.local_addr_state }}
            {{ person.student.local_addr_5digit_zip }}
            {{ person.student.local_addr_country }}
          </address>
        </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue variant="address">
        <template #key>Permanent Address</template>
        <template #value>
          <address>
            {{ person.student.perm_addr_line1 }}
            {{ person.student.perm_addr_line2 }},
            {{ person.student.perm_addr_city }},
            {{ person.student.perm_addr_state }}
            {{ person.student.perm_addr_5digit_zip }}
            {{ person.student.perm_addr_country }}
          </address>
        </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue variant="address">
        <template #key>Parent Address</template>
        <template #value>
          <address>
            {{ person.student.parent_addr_line1 }}
            {{ person.student.parent_addr_line2 }},
            {{ person.student.parent_addr_city }},
            {{ person.student.parent_addr_state }}
            {{ person.student.parent_addr_5digit_zip }},
            {{ person.student.parent_addr_country }}
          </address>
        </template>
      </KeyValue>
    </li>
  </ul>
</template>

<script>
import KeyValue from "@/components/_common/key-value.vue";

export default {
  inject: ["mq"],
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  components: {
    KeyValue,
  },
};
</script>
