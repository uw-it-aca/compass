<template>
  <li class="nav-item me-2" role="presentation">
    <button
      class="nav-link text-secondary text-uppercase small border-bottom border-5"
      :class="{ 'active': activeTab }, tabsId + '-link'"
      :id="panelId + '-tab'"
      data-bs-toggle="tab"
      :data-bs-target="'#' + panelId"
      type="button"
      role="tab"
      :aria-controls="panelId"
      :aria-selected="activeTab"
      @keydown.right="moveNext"
      @keydown.left="movePrev"
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
    tabsId: {
      // must match tab panelId
      type: [String, Number],
      required: true,
    },
    activeTab: {
      type: Boolean,
      required: false,
    },
  },
  computed: {
    elements() {
      // get elements by custon className by concat tabsId and -link (i.e. tabsId-link )
      return document.getElementsByClassName(this.tabsId + '-link');
    },
  },
  methods: {
    findIndex(target) {
      return [].findIndex.call(this.elements, (e) => e === target);
    },
    moveTab(index) {
      if (this.elements[index]) {
        // focus and click on tab
        this.elements[index].focus();
        this.elements[index].click();
      }
    },
    moveNext(event) {
      const index = this.findIndex(event.target);
      this.moveTab(index + 1);
    },
    movePrev(event) {
      const index = this.findIndex(event.target);
      this.moveTab(index - 1);
    },
  },
};
</script>
