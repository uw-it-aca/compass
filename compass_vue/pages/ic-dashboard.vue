// ic-visits.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <h1>Instructional Center Dashboard</h1>
      <studentvisitsearch />
      <visitfileoperations />
      <activeicvisits />
    </template>
  </layout>
</template>

<script>
import Layout from "@/layouts/default.vue";
import ActiveICVisits from "@/components/ic-dashboard/active-visits.vue";
import StudentVisitSearch from "@/components/ic-dashboard/student-visit-search.vue";
import VisitFileOperations from "@/components/ic-dashboard/visit-file-operations.vue";

export default {
  name: "ICDashboardPage",
  components: {
    layout: Layout,
    activeicvisits: ActiveICVisits,
    studentvisitsearch: StudentVisitSearch,
    visitfileoperations: VisitFileOperations,
  },
  data() {
    return {
      pageTitle: "Instructional Center Dashboard",
      isLoading: true,
    };
  },
};
</script>
