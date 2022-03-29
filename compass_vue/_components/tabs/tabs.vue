<template>
  <ul class="nav nav-lines mb-3" :id="tabsId" role="tablist">
    <slot name="items">
      <!-- axdd-tab-button and uw-tab-dropdown components with panelId-->
    </slot>
  </ul>

  <div class="tab-content" :id="tabsId + 'Content'">
    <slot name="panels">
      <!-- axdd-tab-panel components with panelId matching tabs-->
    </slot>
  </div>
</template>

<script>
export default {
  props: {
    tabsId: {
      // must match tab panelId
      type: [String, Number],
      required: true,
    },
  },
};
</script>

<style lang="scss">

// creates a custom bootstrap tab style
.nav-lines {

  border-bottom: 1px solid #dee2e6;

  .nav-link {
    background: none;
    border: none;
    color: gray;
    margin-bottom: -1px;

  }

  .nav-link.active {
    border-color: #000 !important;
    color: #000 !important;
  }

  .nav-link:hover {
    border-color: #333 !important;
    color: #333 !important;
  }

}

</style>
