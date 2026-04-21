// ic-visits.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <h1>Instructional Center Dashboard</h1>
      <activeicvisits />
    </template>
  </layout>
</template>

<script>
import Layout from "@/layouts/default.vue";
import ActiveICVisits from "@/components/ic-dashboard/active-visits.vue";

export default {
  name: "ICDashboardPage",
  components: {
    layout: Layout,
    activeicvisits: ActiveICVisits,
  },
  data() {
    return {
      pageTitle: "Instructional Center Dashboard",
      isLoading: true,
    };
  },
};
</script>
