// reports.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <h2>Upload Batch Affiliations</h2>

      <div class="row my-4 small">
        <div class="col">
          <div class="bg-light p-3 rounded-3">
            <div class="d-flex">
              <div class="me-3">
                <label for="formFile" class="form-label fw-bold"
                  >Select students</label
                >
                <input class="form-control" type="file" id="formFile" />
              </div>
              <div class="me-3">
                <p>Select Affliations</p>
                <select class="form-select" aria-label="Default select example">
                  <option selected disabled>Choose one...</option>
                  <option value="1">CAMP</option>
                  <option value="2">TRIO-SSS</option>
                  <option value="3">Champions</option>
                </select>
              </div>
              <div>
                <p>Select Cohort</p>
                <select class="form-select" aria-label="Default select example">
                  <option selected disabled>Choose one...</option>
                  <option value="1">2024-2025</option>
                  <option value="2">2023-2024</option>
                  <option value="3">2022-2023</option>
                </select>
              </div>
            </div>
            <div class="text-end">
              <button
                type="button"
                class="btn btn-sm fs-7 btn-outline-dark-beige rounded"
                @click="saveFilterPreferences"
              >
                Process Batch
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="row my-4">
        <div class="col">asdfasdf</div>
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
