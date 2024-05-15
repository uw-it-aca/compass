// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <h2>Upload Batch Affiliations</h2>
      <div class="d-flex">
        <div class="mb-3">
          <label for="formFile" class="form-label">Select students</label>
          <input class="form-control" type="file" id="formFile" />
        </div>
        <div>
          <p>Select Affliations</p>
        </div>
        <div><p>Select Cohort</p></div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "@/layout.vue";

export default {
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Affiliations",
      isLoading: true,
    };
  },
};
</script>
