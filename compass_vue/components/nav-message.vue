<template>
  <div class="text-light my-3">
    <div class="text-light-gray bg-dark-purple rounded-3 p-3 small">
      <div class="mb-2">
        <i class="bi bi-exclamation-triangle-fill me-2"></i>System Messages
      </div>
      <ul class="list-unstyled m-0">
        <li
          v-for="(msg, index) in messages"
          :key="index"
          v-html="msg"
          class="mt-2"
        ></li>
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
