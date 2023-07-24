<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Immigration
  </div>
  <ul class="list-unstyled m-0 mb-3 small">
    <li>
      <KeyValue>
        <template #key>Citizenship</template>
        <template #value>
          {{ person.student.citizen_country }}
        </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue>
        <template #key>Visa Type</template>
        <template #value>
          <span v-if="person.student.visa_type">
            {{ person.student.visa_type }}
          </span>
          <span v-else>N/A</span>
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
