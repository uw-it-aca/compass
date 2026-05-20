// visit-file-operations.vue
<template>
  <button
    data-bs-toggle="modal"
    data-bs-target="#importDataModal"
    class="btn btn-sm btn-outline-primary"
  >
    Import Data
  </button>
  <button>Export Data</button>

  <!-- Modal for importing data -->
  <div
    id="importDataModal"
    ref="importDataModal"
    class="modal fade"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content container">
        <div class="modal-header">
          <h5 class="modal-title">Instructional Center Data Upload</h5>
        </div>
        <form
        v-if="!isLoadingOptions"
        @submit.prevent="handleUpload"
        >
          Program Area*
          <select
            class="form-select mb-3"
            required
            v-model="importOptions.visit_type"
          >
            <option value="" disabled selected>Select a program area</option>
            <option
              v-for="option in visitOptions.program_areas"
              :key="option.id"
              :value="option.name"
            >
              {{ option.name }}
            </option>
          </select>
          Tutoring Options*
          <select
            class="form-select mb-3"
            required
            v-model="importOptions.tutoring_option"
          >
            <option value="" disabled selected>Select a tutoring option</option>
            <option
              v-for="option in visitOptions.tutoring_options"
              :key="option.id"
              :value="option.name"
            >
              {{ option.name }}
            </option>
          </select>
          Student File*
          <input
            class="form-control mb-3"
            type="file"
            accept=".csv,"
            @change="addFile"
            required
          />
          <input id="checkin_date" v-model="importOptions.date" type="date" />
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">Upload</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { uploadVisitFile, getICVisitOptions } from "@/utils/data";

export default {
  name: "VisitFileOperations",
  setup: function () {
    return {
      uploadVisitFile,
      getICVisitOptions,
    };
  },
  data() {
    return {
      importOptions: {
        file: null,
        visit_type: "Program Area 1",
        tutoring_option: "Tutoring Option 2",
        date: "2026-05-14",
      },
      isLoadingOptions: true,
      visitOptions: null,
    };
  },
  mounted() {
    this.$refs.importDataModal.addEventListener(
      "shown.bs.modal",
      this.loadSVisitOptions,
    );
    this.$refs.importDataModal.addEventListener(
      "hidden.bs.modal",
      this.resetForm,
    );
  },
  methods: {
    addFile(e) {
      this.importOptions.file = e.target.files[0];
    },
    loadSVisitOptions: function () {
      // Use a bad regid so courses are empty, other options should still load
      getICVisitOptions("NOCOURSESREGID")
        .then((response) => {
          if (response) {
            this.visitOptions = response;
            this.errorResponse = null;
          }
        })
        .catch((error) => {
          this.errorResponse = error.data;
        })
        .finally(() => {
          this.isLoadingOptions = false;
        });
    },
    resetForm: function () {
      this.importOptions = {
        file: null,
        visit_type: null,
        tutoring_option: null,
        date: null,
      };
      this.visitOptions = null;
      this.isLoadingOptions = true;
    },
    handleUpload: function () {
      if (
        this.importOptions.file &&
        this.importOptions.visit_type &&
        this.importOptions.tutoring_option &&
        this.importOptions.date
      ) {
        console.log("Uploading file with options:", this.importOptions);
        this.uploadVisitFile(this.importOptions)
          .then((response) => {
            // Handle successful upload, maybe show a success message
            console.log("Upload successful:", response);
          })
          .catch((error) => {
            // Handle upload error, maybe show an error message
            console.error("Upload failed:", error);
          });
      } else {
        // Handle form validation error, maybe show a warning message
        console.warn("Please fill in all required fields.");
      }
    },
  },
};
</script>
