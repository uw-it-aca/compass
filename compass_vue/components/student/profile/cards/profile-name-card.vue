<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Legal Name
  </div>
  <ul class="list-unstyled m-0 small mb-3">
    <li>
      <KeyValue>
        <template #key>Full Name </template>
        <template #value> {{ person.full_name }} </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue>
        <template #key>First Name </template>
        <template #value> {{ person.first_name }} </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue>
        <template #key>Last Name </template>
        <template #value> {{ person.surname }} </template>
      </KeyValue>
    </li>
  </ul>
</template>

<script>
import KeyValue from "../../../_common/key-value.vue";

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
  data() {
    return {
      // add data for first and last name
    };
  },
};
</script>
