// visit-file-operations.vue
<template>
  <button
    data-bs-toggle="modal"
    data-bs-target="#importDataModal"
    class="btn btn-sm btn-outline-primary"
  >
    Import Data
  </button>
  <a
    href="/api/internal/visits/file/"
    download="compass_visit_data.csv"
    class="btn btn-sm btn-outline-primary"
  >
    Export Data
  </a>

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
        <div v-if="isUploading" class="d-flex justify-content-center my-5">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Uploading...</span>
          </div>
        </div>
        <div v-else >
        <form v-if="!isLoadingOptions" @submit.prevent="handleUpload">
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
        <!-- Upload Error -->
        <div
          v-if="uploadErrorResponse"
          class="alert alert-danger mt-3"
          role="alert"
        >
          {{ uploadErrorResponse }}
        </div>
      </div>
    </div>
  </div>
  <!-- End of Modal -->
</template>

<script>
import { uploadVisitFile, getICVisitOptions } from "@/utils/data";

import { Modal } from "bootstrap";

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
        visit_type: "",
        tutoring_option: "",
        date: "",
      },
      isLoadingOptions: true,
      visitOptions: null,
      uploadErrorResponse: null,
      isUploading: false,
    };
  },
  mounted() {
    this.$refs.importDataModal.addEventListener(
      "shown.bs.modal",
      this.loadvisitoptions,
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
    loadvisitoptions: function () {
      // Use a bad regid so courses are empty, other options should still load
      getICVisitOptions("NOCOURSESREGID")
        .then((response) => {
          if (response) {
            this.visitOptions = response;
            this.uploadErrorResponse = null;
          }
        })
        .catch((error) => {
          this.uploadErrorResponse = error.data;
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
      this.uploadErrorResponse = null;
      this.isUploading = false;
    },
    handleUpload: function () {
      if (
        this.importOptions.file &&
        this.importOptions.visit_type &&
        this.importOptions.tutoring_option &&
        this.importOptions.date
      ) {
        this.isUploading = true;
        this.uploadVisitFile(this.importOptions)
          .then((response) => {
            this.resetForm();
            var modalElement = Modal.getInstance(this.$refs.importDataModal);
            modalElement.hide();

          })
          .catch((error) => {
            this.isUploading = false;
            this.uploadErrorResponse = error.data.message;
          });
      } else {
        // Handle form validation error, maybe show a warning message
        this.uploadErrorResponse =
        "Please fill in all required fields and select a file.";
      }
    },
  },
};
</script>
