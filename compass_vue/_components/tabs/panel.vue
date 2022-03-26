<template>
  <div class="tab-pane fade" :id="panelId" role="tabpanel" :aria-labelledby="panelId + '-tab'">
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: {
    panelId: {
      // must match tab panelId
      type: [String, Number],
      required: true,
    },
  },
};
</script>
