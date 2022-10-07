<template>
  <div
    :class="[
      mq.lgMinus && variant != 'address'
        ? 'justify-content-between d-flex'
        : '',
      mq.lgPlus && variant != 'address' ? 'd-flex' : '',
    ]"
    class="mx-2"
  >
    <div v-if="$slots['key']" class="fw-bold text-nowrap me-2">
      <slot name="key"></slot>
    </div>
    <div v-if="$slots['value']" :class="[variant == 'address' ? '' : '']">
      <slot name="value"></slot>
    </div>
  </div>
</template>

<script>
export default {
  inject: ["mq"],
  props: {
    variant: {
      type: String,
      default: "standard",
    },
  },
  data() {
    return {};
  },
};
</script>
