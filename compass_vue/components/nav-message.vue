<template>
  <div class="text-light my-3">
    <div class="bg-white bg-opacity-10 text-white rounded-3 p-3 small">
      <div class="mb-2">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>System Messages
      </div>
      <ul class="list-unstyled m-0">
        <li
          v-for="(msg, index) in messages"
          :key="index"
          class="mt-2"
          v-html="msg">
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messages: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
