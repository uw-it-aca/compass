// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>403 Forbidden</template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "403 Forbidden",
    };
  },
};
</script>

<style lang="scss"></style>
