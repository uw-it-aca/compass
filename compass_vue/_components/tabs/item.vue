<template>
<li class="nav-item" role="presentation">
  <button
    class="nav-link"
    :class="{ 'active': activeTab }"
    :id="panelId + '-tab'"
    data-bs-toggle="tab"
    :data-bs-target="'#' + panelId"
    type="button"
    role="tab"
    :aria-controls="panelId"
    aria-selected="true"
  >
    <slot></slot>
  </button>
  </li>
</template>

<script>
export default {
  props: {
    panelId: {
      // must match tab panelId
      type: [String, Number],
      required: true,
    },
    activeTab: {
      type: Boolean,
      required: false,
    }
  },
};
</script>
