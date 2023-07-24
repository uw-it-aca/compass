<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Residency
  </div>
  <ul class="list-unstyled m-0 small">
    <li class="mb-3">
      <KeyValue>
        <template #key>Status</template>
        <template #value>
          {{ person.student.resident_desc }}
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
