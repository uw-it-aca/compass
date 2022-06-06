// settings.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      this page is for Admin, Support, and Group Admin roles only</template
    >
  </layout>
</template>

<script>
import Layout from "../layout.vue";
import dataMixin from "../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Settings",
      isLoading: true,
    };
  },
};
</script>

<style lang="scss"></style>
