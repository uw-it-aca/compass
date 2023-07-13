<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Emergency Contact
  </div>
  <ul class="list-unstyled m-0 small">
    <li>
      <KeyValue>
        <template #key>Name</template>
        <template #value>
          {{ person.student.emergency_name }}
        </template>
      </KeyValue>
    </li>
    <li>
      <KeyValue>
        <template #key>Phone</template>
        <template #value>
          {{ person.student.emergency_phone }}
        </template>
      </KeyValue>
    </li>
    <li>
      <span v-if="person.student.emergency_email.length > 25">
        <KeyValue variant="address">
          <template #key>Email</template>
          <template #value>
            {{ person.student.emergency_email }}
          </template>
        </KeyValue>
      </span>
      <span v-else>
        <KeyValue>
          <template #key>Email</template>
          <template #value>
            {{ person.student.emergency_email }}
          </template>
        </KeyValue>
      </span>
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
};
</script>
