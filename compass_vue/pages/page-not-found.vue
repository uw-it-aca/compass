// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>404 Page Not Found</template>
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
      pageTitle: "404 Not Found",
    };
  },
};
</script>

<style lang="scss"></style>
