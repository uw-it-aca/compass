<template>
  <div :class="[mq.lgMinus ? 'justify-content-between' : '']" class="d-flex">
    <div v-if="$slots['key']" class="fw-bold text-nowrap me-2">
      <slot slot name="key"></slot>
    </div>
    <div v-if="$slots['value']">
      <slot slot name="value"></slot>
    </div>
  </div>
  <div>
    <div v-if="$slots['kAdress']" class="fw-bold text-nowrap me-2">
      <slot slot name="kAdress"></slot>
    </div>
    <div v-if="$slots['vAdress']">
      <slot slot name="vAdress"></slot>
    </div>
  </div>
</template>

<script>
export default {
  inject: ["mq"],
  data() {
    return {};
  },
};
</script>
