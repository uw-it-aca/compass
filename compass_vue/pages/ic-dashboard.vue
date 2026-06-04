// ic-visits.vue

<template>
  <layout :page-title="pageTitle">
    <template #content>
      <h1 class= "display-5 fw-bold ff-encode-sans pt-2">
      Instructional Center Dashboard
      </h1>
      <div class= "card border-0 bg-body-tertiary rounded-3">
        <div class= "row justify-content-between align-items-center m-2 py-2 ">
          <div class="col-3">
            <div>
              <studentvisitsearch @visit-created="handleVisitCreated"/>
            </div>
          </div>
          <div class="col-auto">
            <visitfileoperations />
          </div>
        </div>
      </div>
      <activeicvisits ref="activeVisitsComp"/>
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
  methods: {
    handleVisitCreated() {
      // Refresh the active visits list when a new visit is created
      this.$refs.activeVisitsComp.handleVisitUpdated();
    },
  },
};
</script>
