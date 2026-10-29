// visit-file-operations.vue
<template>
  <button
    data-bs-toggle="modal"
    data-bs-target="#importDataModal"
    class="btn btn-sm btn-subdued-primary me-3"
  >
    <i class="bi bi-upload me-2"></i>Import Data
  </button>

  <button
    data-bs-toggle="modal"
    data-bs-target="#exportDataModal"
    class="btn btn-sm btn-subdued-primary"
  >
    <i class="bi bi-download me-2"></i>Export Data
  </button>

  <!-- Modal for exporting data -->
  <div
    id="exportDataModal"
    class="modal fade"
    tabindex="-1"
    aria-labelledby="visit-export-title"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 id="contactModalLabel" class="modal-title fw-bold">
            Instructional Center Data Export
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" :aria-busy="isDownloading">
          <STabsList :tabs-id="'visit-export'">
            <STabsItem
              :tabs-id="'visit-export'"
              :panel-id="'visit-export-range'"
              :active-tab="true"
            >
              Custom Date Range
            </STabsItem>
            <STabsItem
              :tabs-id="'visit-export'"
              :panel-id="'visit-export-month'"
            >
              Monthly Export
            </STabsItem>
          </STabsList>

          <STabsDisplay :tabs-id="'visit-export'">
            <!--custom date range-->
            <STabsPanel :panel-id="'visit-export-range'" :active-panel="true">
              <form class="mt-4" @submit.prevent="handleDownload()">
                <div class="row g-3 pb-3">
                  <div class="col-12 col-sm-6">
                    <label for="visit-export-start" class="form-label fw-bold">
                      Check-in Start Date <span style="color: red">*</span>
                    </label>
                    <input
                      id="visit-export-start"
                      v-model="exportOptions.start_date"
                      type="date"
                      class="form-control w-100"
                      @change="adjustExportEndDate"
                      :min="earliestExportDate"
                      aria-describedby="visit-export-range-limit"
                      :disabled="isDownloading"
                      required
                    />
                  </div>
                  <div class="col-12 col-sm-6">
                    <label for="visit-export-end" class="form-label fw-bold">
                      Check-in End Date <span style="color: red">*</span>
                    </label>
                    <input
                      id="visit-export-end"
                      v-model="exportOptions.end_date"
                      type="date"
                      class="form-control w-100"
                      :min="
                        exportOptions.start_date &&
                        exportOptions.start_date > earliestExportDate
                          ? exportOptions.start_date
                          : earliestExportDate
                      "
                      :max="exportEndMax"
                      aria-describedby="visit-export-range-limit"
                      :disabled="isDownloading"
                      required
                    />
                  </div>
                </div>
                <div id="visit-export-range-limit" class="form-text">
                  Maximum date range: 1 year.
                </div>
                <div class="d-flex justify-content-end mt-4">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="isDownloading"
                  >
                    <span
                      v-if="activeExport === 'range'"
                      class="spinner-border spinner-border-sm me-2"
                      aria-hidden="true"
                    ></span>
                    Download CSV
                  </button>
                </div>
              </form>
            </STabsPanel>

            <!--monthly Export-->
            <STabsPanel :panel-id="'visit-export-month'">
              <form
                class="mt-4"
                @submit.prevent="handleMonthDownload(exportMonth)"
              >
                <div class="row g-3 pb-4">
                  <div class="col-12 col-sm-6">
                    <label for="visit-export-year" class="form-label fw-bold">
                      Year <span style="color: red">*</span>
                    </label>
                    <select
                      id="visit-export-year"
                      v-model.number="exportYear"
                      class="form-select w-100"
                      :disabled="isDownloading"
                    >
                      <option
                        v-for="year in exportYears"
                        :key="year"
                        :value="year"
                      >
                        {{ year }}
                      </option>
                    </select>
                  </div>
                  <div class="col-12 col-sm-6">
                    <label for="visit-export-month" class="form-label fw-bold">
                      Month <span style="color: red">*</span>
                    </label>
                    <select
                      id="visit-export-month"
                      v-model.number="exportMonth"
                      class="form-select w-100"
                      :disabled="isDownloading"
                    >
                      <option
                        v-for="month in exportMonths"
                        :key="month.index"
                        :value="month.index"
                        :disabled="month.isFuture"
                      >
                        {{ month.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="d-flex justify-content-end mt-4">
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="
                      isDownloading || exportMonths[exportMonth]?.isFuture
                    "
                  >
                    <span
                      v-if="activeExport === `${exportYear}-${exportMonth}`"
                      class="spinner-border spinner-border-sm me-2"
                      aria-hidden="true"
                    ></span>
                    Download CSV
                  </button>
                </div>
              </form>
            </STabsPanel>
          </STabsDisplay>
          <div
            v-if="downloadErrorResponse"
            class="alert alert-danger mt-3 mb-0"
            role="alert"
          >
            {{ downloadErrorResponse }}
          </div>
        </div>
        <div
          id="visit-export-status"
          class="visually-hidden"
          role="status"
          aria-atomic="true"
        >
          {{ exportStatus }}
        </div>
      </div>
    </div>
  </div>

  <!-- Modal for importing data -->
  <div
    id="importDataModal"
    ref="importDataModal"
    class="modal fade"
    tabindex="-1"
    aria-labelledby="visit-import-title"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 id="contactModalLabel" class="modal-title fw-bold">
            Instructional Center Data Upload
          </h5>
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
        <div v-else class="modal-body">
          <form v-if="!isLoadingOptions" @submit.prevent="handleUpload">
            <div class="row mb-3">
              <div class="col">
                <label for="validationCustom02" class="form-label fw-bold">
                  Program Area <span style="color: red">*</span>
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
                  Tutoring Options <span style="color: red">*</span>
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

            <div class="row mb-3">
              <div class="col">
                <label for="validationCustom02" class="form-label fw-bold">
                  Check-in Date <span style="color: red">*</span>
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
                  Student File <span style="color: red">*</span>
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
            class="btn btn-outline-primary py-2"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary py-2">Upload</button>
          <!-- Upload Error -->
          <div
            v-if="uploadErrorResponse"
            class="alert alert-danger small m-0"
            role="alert"
            aria-live="polite"
            aria-atomic="true"
          >
            <i class="bi-exclamation-octagon-fill me-1"></i
            >{{ uploadErrorResponse }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { uploadVisitFile, getICVisitOptions } from "@/utils/data";

  import { Modal } from "bootstrap";
  import dayjs from "dayjs";
  import { STabsDisplay, STabsPanel, STabsList, STabsItem } from "solstice-vue";

  export default {
    name: "VisitFileOperations",
    components: {
      STabsDisplay,
      STabsPanel,
      STabsList,
      STabsItem,
    },
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
        exportOptions: {
          start_date: dayjs().subtract(29, "day").format("YYYY-MM-DD"),
          end_date: dayjs().format("YYYY-MM-DD"),
        },
        isDownloading: false,
        downloadErrorResponse: null,
        today: dayjs().format("YYYY-MM-DD"),
        exportYear: dayjs().year(),
        exportMonth: dayjs().month(),
        earliestExportDate: "2008-01-01",
        activeExport: null,
        exportStatus: "",
        exportAbortController: null,
      };
    },
    computed: {
      exportEndMax() {
        return this.exportOptions.start_date
          ? dayjs(this.exportOptions.start_date)
              .add(365, "day")
              .format("YYYY-MM-DD")
          : undefined;
      },
      exportYears() {
        const currentYear = dayjs(this.today).year();
        return Array.from(
          { length: currentYear - dayjs(this.earliestExportDate).year() + 1 },
          (_, index) => currentYear - index,
        );
      },
      exportMonths() {
        const yearStart = dayjs(`${this.exportYear}-01-01`);
        return Array.from({ length: 12 }, (_, index) => {
          const month = yearStart.month(index);
          return {
            index,
            label: month.format("MMM"),
            name: month.format("MMMM"),
            isFuture: month.isAfter(dayjs(this.today), "month"),
          };
        });
      },
    },
    watch: {
      exportYear() {
        // If the selected month is in the future for the new year, fall back to the current month
        if (this.exportMonths[this.exportMonth]?.isFuture) {
          this.exportMonth = dayjs(this.today).month();
        }
      },
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
    beforeUnmount() {
      this.exportAbortController?.abort();
    },
    methods: {
      adjustExportEndDate() {
        this.exportStatus = "";
        const { start_date, end_date } = this.exportOptions;
        if (!start_date || !end_date) return;
        if (end_date < start_date) {
          this.exportOptions.end_date = start_date;
        } else if (end_date > this.exportEndMax) {
          this.exportOptions.end_date = this.exportEndMax;
        }
        if (this.exportOptions.end_date !== end_date) {
          this.exportStatus = `End date adjusted to ${dayjs(this.exportOptions.end_date).format("MMMM D, YYYY")} to keep the date range valid.`;
        }
      },
      handleMonthDownload(monthIndex) {
        if (this.isDownloading) return;
        const month = dayjs(`${this.exportYear}-01-01`).month(monthIndex);
        if (month.isAfter(dayjs(this.today), "month")) return;
        return this.handleDownload(
          {
            start_date: month.startOf("month").format("YYYY-MM-DD"),
            end_date: month.endOf("month").format("YYYY-MM-DD"),
          },
          `${this.exportYear}-${monthIndex}`,
        );
      },
      async handleDownload(options = this.exportOptions, source = "range") {
        if (this.isDownloading) return;
        this.downloadErrorResponse = null;
        this.exportStatus = "";
        const { start_date, end_date } = options;
        if (!start_date || !end_date || end_date < start_date) {
          this.downloadErrorResponse = "Select a valid start and end date.";
          return;
        }
        if (start_date < this.earliestExportDate) {
          this.downloadErrorResponse =
            "Visit exports are available from January 1, 2008.";
          return;
        }
        if (dayjs(end_date).diff(dayjs(start_date), "day") >= 366) {
          this.downloadErrorResponse =
            "Export date range cannot exceed 366 days.";
          return;
        }
        this.isDownloading = true;
        this.activeExport = source;
        this.exportStatus = "Preparing export...";
        const controller = new AbortController();
        this.exportAbortController = controller;
        let objectUrl;
        try {
          const query = new URLSearchParams({ start_date, end_date });
          const response = await fetch(`/api/internal/visits/file/?${query}`, {
            credentials: "same-origin",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            signal: controller.signal,
          });
          if (controller.signal.aborted) return;
          if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
              throw new Error(
                "Your session may have expired or access was denied. Refresh the page and sign in again before exporting.",
              );
            }
            let message = "Unable to download visits. Please try again.";
            try {
              const error = await response.json();
              if (typeof error === "string") message = error;
            } catch {}
            throw new Error(message);
          }
          if (!response.headers.get("Content-Type")?.startsWith("text/csv")) {
            throw new Error(
              "Unable to download visits. Refresh the page and try again.",
            );
          }
          const blob = await response.blob();
          if (controller.signal.aborted) return;
          objectUrl = URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = objectUrl;
          link.download = `compass_visit_data_${start_date}_${end_date}.csv`;
          document.body.appendChild(link);
          link.click();
          link.remove();
          this.exportStatus =
            "Export ready. CSV download requested in your browser.";
        } catch (error) {
          this.exportStatus = "";
          if (!controller.signal.aborted) {
            this.downloadErrorResponse =
              error.message || "Unable to download visits. Please try again.";
          }
        } finally {
          if (objectUrl) setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
          this.isDownloading = false;
          this.activeExport = null;
          this.exportAbortController = null;
        }
      },
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
