<template>
  <div
    v-if="mq.xlPlus"
    class="text-uppercase text-dark-beige fs-8 fw-bold mb-2"
  >
    Athletics
  </div>
  <ul class="list-unstyled m-0 small">
    <li class="mb-3">
      <KeyValue>
        <template #key>Sports</template>
        <template #value>
          <span
            v-for="(sport, index) in person.student.sports"
            :key="sport.code"
          >
            {{ sport.sport_code }}
            <span v-if="index + 1 < person.student.sports.length">, </span>
          </span>
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
