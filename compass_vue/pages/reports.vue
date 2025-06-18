// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content> this page is for Manager roles only</template>
  </layout>
</template>

<script>
import Layout from "@/layout.vue";

export default {
  name: "ReportsPage",
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Reports",
      isLoading: true,
    };
  },
};
</script>
