// visit-file-operations.vue
<template>
  <button
    data-bs-toggle="modal"
    data-bs-target="#importDataModal"
    class="btn btn-sm btn-subdued-primary me-3"
  >
    <i class="bi bi-upload me-2"></i>Import Data
  </button>
  <button class="btn btn-sm btn-subdued-primary" @click="handleDownload">
    <i class="bi bi-download me-2"></i>Export Data
  </button>

  <!-- Modal for importing data -->
  <div
    id="importDataModal"
    ref="importDataModal"
    class="modal fade"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h3 id="contactModalLabel" class="fs-5 fw-bold ff-open-sans m-0">
            Instructional Center Data Upload
          </h3>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div v-if="isUploading" class="d-flex justify-content-center my-5">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Uploading...</span>
          </div>
        </div>
        <div v-else class="modal-body p-4">
          <form v-if="!isLoadingOptions" @submit.prevent="handleUpload">
            <div class="row pb-4">
              <div class="col">
                <label for="validationCustom02" class="form-label fw-bold">
                  Program Area *
                </label>
                <select
                  class="form-select"
                  required
                  v-model="importOptions.visit_type"
                >
                  <option value="" disabled selected>
                    Select a program area
                  </option>
                  <option
                    v-for="option in visitOptions.program_areas"
                    :key="option.id"
                    :value="option.name"
                  >
                    {{ option.name }}
                  </option>
                </select>
              </div>

              <div class="col">
                <label for="validationCustom02" class="form-label fw-bold">
                  Tutoring Options *
                </label>
                <select
                  class="form-select"
                  required
                  v-model="importOptions.tutoring_option"
                >
                  <option value="" disabled selected>
                    Select a tutoring option
                  </option>
                  <option
                    v-for="option in visitOptions.tutoring_options"
                    :key="option.id"
                    :value="option.name"
                  >
                    {{ option.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="row">
              <div class="col">
                <label for="validationCustom02" class="form-label fw-bold">
                  Date *
                </label>

                <input
                  id="checkin_date"
                  v-model="importOptions.date"
                  type="date"
                  class="form-control"
                />
              </div>

              <div class="col">
                <label for="validationCustom02" class="form-label fw-bold">
                  Student File *
                </label>
                <input
                  class="form-control"
                  type="file"
                  accept=".csv,"
                  @change="addFile"
                  required
                />
              </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-outline-primary rounded-3 mx-2"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary rounded-3 mx-2">
            Upload
          </button>
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
  <! -- End of Modal -->

  <!-- Download Error -->
  <div
    v-if="downloadErrorResponse"
    class="alert alert-danger mt-3"
    role="alert"
  >
    {{ downloadErrorResponse }}
  </div>
  <!-- End of Download Error -->
  <!-- Downloading spinner -->
  <div v-if="isDownloading" class="d-flex my-5">
    Downloading Visits
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Downloading...</span>
    </div>
  </div>
  <!-- End of downloading spinner -->
</template>

<script>
  import {
    uploadVisitFile,
    getICVisitOptions,
    downloadVisitFile,
  } from "@/utils/data";

  import { Modal } from "bootstrap";

  export default {
    name: "VisitFileOperations",
    setup: function () {
      return {
        uploadVisitFile,
        getICVisitOptions,
        downloadVisitFile,
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
        downloadErrorResponse: null,
        isDownloading: false,
        uploadErrorResponse: null,
        isUploading: false,
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
      handleDownload: function () {
        this.isDownloading = true;
        this.downloadVisitFile()
          .then((response) => {
            const blob = new Blob([response], { type: "text/csv" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "compass_visit_data.csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            this.downloadErrorResponse = null;
            this.isDownloading = false;
          })
          .catch((error) => {
            // Handle download error, maybe show an error message
            this.downloadErrorResponse = error.data.message;
            this.isDownloading = false;
          });
      },
    },
  };
</script>
