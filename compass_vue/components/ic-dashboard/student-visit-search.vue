// student-visit-search.vue

<template>
  <label for="validationCustom02" class="form-label fw-bold">
    Search all students
  </label>
  <form onsubmit="return false;">
    <div class="input-group">
      <input
        v-model="searchValue"
        type="text"
        :maxlength="maxLength"
        class="form-control form-control-sm"
        aria-label="Student number or UW netid"
      />
      <button
        data-bs-toggle="modal"
        data-bs-target="#studentSearchModal"
        class="btn btn-sm btn-outline-primary"
        :disabled="!validQuery"
      >
        Search
      </button>
      <div class="form-text">Enter a student number or UW Netid</div>
    </div>
  </form>

  <div
    id="studentSearchModal"
    ref="studentSearchModal"
    class="modal fade"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h3 id="contactModalLabel" class="fs-5 fw-bold ff-open-sans m-0">
            Instructional Center Check In
          </h3>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div v-if="!validQuery">Invalid student identifier</div>
          <div v-else class="row">
            <!-- left column -->
            <!-- Need to fix error message -->
            <div v-if="searchError" class="alert alert-danger col">
              Could not find a student matching "{{ searchValue }}". Please try
              again.
            </div>

            <div v-else-if="person" class="student-bio col">
              <div v-lazyload class="mb-3 text-center">
                <img
                  :data-url="person.photo_url"
                  :alt="person.display_name + ' profile picture'"
                  class="img-profile rounded-circle border border-3"
                  @error="
                    $event.target.src = '/static/compass/img/placeholder.png'
                  "
                />
              </div>
              <div class="text-center mb-3">
                <span
                  v-if="isICEligible"
                  class="badge text-bg-secondary text-success-emphasis bg-success-subtle rounded-pill fw-semibold me-1"
                  >IC Eligible</span
                >
                <span
                  v-else
                  class="badge text-bg-secondary text-danger-emphasis bg-danger-subtle rounded-pill fw-semibold me-1"
                  >Not Eligible</span
                >
              </div>
              <h4 class="fs-4 fw-semibold ff-encode-sans mb-3 text-center">
                {{ person.full_name }}
              </h4>
              <p class="text-center m-0">
                {{ person.student.student_number }}, {{ person.uwnetid }}
                <br />
                {{ person.student.local_phone_number }}
              </p>
            </div>

            <!-- right column -->
            <div v-if="rightColHasData" class="col">
              <!-- IC Eligibility Approval -->
              <div v-if="displayMode === 'visits'">
                <studenvisitsummary :studentVisits="studentVisitData" />
              </div>
              <div v-else-if="displayMode === 'not_eligible'">
                Student is not eligible to use the Instructional Center. Would
                you like to approve their eligibility?
                <button
                  class="btn btn-primary ms-3"
                  @click="addICEligibility()"
                >
                  Approve
                </button>
              </div>

              <!-- IC Check In -->
              <div v-else-if="displayMode === 'checkin'">
                <form v-if="!isLoadingOptions">
                  <label for="validationCustom02" class="form-label fw-bold">
                    Program Area *
                  </label>
                  <select
                    class="form-select mb-3"
                    required
                    v-model="checkInData.programArea"
                  >
                    <option value="" disabled selected>
                      Select a program area
                    </option>
                    <option
                      v-for="option in visitOptions.program_areas"
                      :key="option.id"
                      :value="option.id"
                    >
                      {{ option.name }}
                    </option>
                  </select>

                  <label for="validationCustom02" class="form-label fw-bold">
                    Tutoring Options *
                  </label>
                  <select
                    class="form-select mb-3"
                    required
                    v-model="checkInData.tutoringOption"
                  >
                    <option value="" disabled selected>
                      Select a tutoring option
                    </option>
                    <option
                      v-for="option in visitOptions.tutoring_options"
                      :key="option.id"
                      :value="option.id"
                    >
                      {{ option.name }}
                    </option>
                  </select>

                  <label for="validationCustom02" class="form-label fw-bold">
                    Course or Other Writing Services *
                  </label>
                  <select
                    class="form-select mb-3"
                    required
                    v-model="checkInData.courseOrWritingService"
                  >
                    <optgroup label="Writing Services">
                      <option value="" disabled selected>
                        Select a course or writing service
                      </option>
                      <option
                        v-for="option in visitOptions.writing_services"
                        :key="option.id"
                        :value="option.id"
                      >
                        {{ option.name }}
                      </option>
                    </optgroup>
                    <optgroup
                      v-if="
                        visitOptions.courses && visitOptions.courses.length > 0
                      "
                      label="Courses"
                    >
                      <option
                        v-for="option in visitOptions.courses"
                        :key="option.id"
                        :value="option.id"
                      >
                        {{ option.name }}
                      </option>
                    </optgroup>
                  </select>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-outline-primary rounded-3 mx-2"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button
            v-if="showCheckinButton"
            class="btn btn-primary rounded-3 mx-2"
            @click="setCheckinMode()"
          >
            Continue
          </button>

          <button
            v-else-if="displayMode === 'checkin'"
            type="button"
            class="btn btn-primary"
            :disabled="!allCreateFieldsSelected"
            @click="createVisit()"
          >
            Check In
          </button>
          <div v-if="createError" class="alert alert-danger mt-3">
            {{ createError.message || "Error creating visit." }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {
    getStudentBySearch,
    getStudentDetail,
    getStudentVisits,
    getStudentEligibility,
    getEligibilities,
    setStudentEligibility,
    getICVisitOptions,
    createICVisit,
  } from "@/utils/data";
  import StudentVisitSummary from "./student-visit-summary.vue";
  import LazyLoad from "@/directives/lazyload";

  export default {
    setup: function () {
      return {
        getStudentBySearch,
        getStudentDetail,
        getStudentVisits,
        getStudentEligibility,
        getEligibilities,
        setStudentEligibility,
        getICVisitOptions,
        createICVisit,
      };
    },
    name: "StudentVisitSearch",
    directives: {
      lazyload: LazyLoad,
    },
    components: {
      studenvisitsummary: StudentVisitSummary,
    },
    data() {
      return {
        searchValue: "",
        maxLength: 32,
        searchError: null,
        validSyskey: null,
        person: null,
        creatingCheckin: false,
        studentVisitData: [],
        studentEligibility: null,
        errorResponse: null,
        isLoadingVisits: true,
        isLoadingOptions: false,
        visitOptions: null,
        checkInData: {
          programArea: "",
          tutoringOption: "",
          courseOrWritingService: "",
        },
        createError: null,
      };
    },
    computed: {
      validQuery: function () {
        return (
          this.searchValue.length >= 2 &&
          this.searchValue.length <= this.maxLength &&
          /^[a-z0-9\-\_\.]+$/.test(this.searchValue)
        );
      },
      isICEligible() {
        if (this.studentEligibility) {
          return this.studentEligibility.some(
            (eligibility) =>
              eligibility.slug === window.icVisitsEligibilitySlug,
          );
        }
      },
      showVisits() {
        return (
          this.person &&
          !this.isLoadingVisits &&
          this.studentVisitData &&
          this.isICEligible
        );
      },
      rightColHasData() {
        return this.person && this.studentEligibility;
      },
      showCheckinButton() {
        return this.showVisits && !this.creatingCheckin;
      },

      displayMode() {
        if (this.person && !this.isICEligible) {
          return "not_eligible";
        } else if (this.creatingCheckin) {
          return "checkin";
        } else {
          return "visits";
        }
      },
      allCreateFieldsSelected() {
        return (
          this.checkInData.programArea &&
          this.checkInData.tutoringOption &&
          this.checkInData.courseOrWritingService
        );
      },
      selectedCourse() {
        return this.visitOptions.courses.find(
          (course) => course.id === this.checkInData.courseOrWritingService,
        );
      },
      selectedWritingService() {
        return this.visitOptions.writing_services.find(
          (service) => service.id === this.checkInData.courseOrWritingService,
        );
      },
    },
    mounted() {
      this.$refs.studentSearchModal.addEventListener(
        "shown.bs.modal",
        this.searchByStudent,
      );
      this.$refs.studentSearchModal.addEventListener(
        "hidden.bs.modal",
        this.resetForm,
      );
    },
    watch: {
      validSyskey(newSyskey) {
        if (newSyskey) {
          this.loadStudent();
        } else {
          this.person = null;
        }
      },
    },
    methods: {
      setCheckinMode: function () {
        this.isLoadingOptions = true;
        this.creatingCheckin = true;
        this.loadStudentVisitOptions();
      },
      resetForm: function () {
        this.searchValue = "";
        this.searchError = null;
        this.validSyskey = null;
      },
      searchByStudent: function () {
        this.searchError = null;
        this.searchValue = this.searchValue.trim().toLowerCase();
        this.getStudentBySearch(this.searchValue)
          .then((response) => {
            this.validSyskey = this.searchValue;
          })
          .catch((err) => {
            this.searchError = { message: "Error fetching student data" };
            this.validSyskey = null;
          });
      },
      loadStudent: function () {
        this.getStudentDetail(this.validSyskey)
          .then((response) => {
            if (response) {
              this.person = response;
              this.errorResponse = null;
              this.loadStudentVisits();
              this.loadStudentEligibility();
            }
          })
          .catch((error) => {
            this.errorResponse = error.data;
          })
          .finally(() => {
            this.isLoadingStudent = false;
          });
      },
      loadStudentEligibility: function () {
        this.getStudentEligibility(this.person.system_key)
          .then((response) => {
            if (response) {
              this.studentEligibility = response;
              this.errorResponse = null;
              this.errorResponse = "bad eligibility error";
            }
          })
          .catch((error) => {
            this.errorResponse = error.data;
          });
      },
      loadStudentVisits: function () {
        this.getStudentVisits(this.person.system_key, true)
          .then((response) => {
            if (response) {
              this.studentVisitData = response;
              this.errorResponse = null;
            }
          })
          .catch((error) => {
            this.errorResponse = error.data;
          })
          .finally(() => {
            this.isLoadingVisits = false;
          });
      },
      addICEligibility: function () {
        this.getEligibilities()
          .then((response) => {
            const icEligibility = response.find(
              (eligibility) =>
                eligibility.slug === window.icVisitsEligibilitySlug,
            );
            if (icEligibility) {
              return this.setStudentEligibility(
                this.person.system_key,
                icEligibility.id,
              );
            } else {
              throw new Error("IC Eligibility not found");
            }
          })
          .then(() => {
            this.loadStudentEligibility();
          })
          .catch((error) => {
            this.errorResponse = error.data || error.message;
          });
      },
      loadStudentVisitOptions: function () {
        getICVisitOptions(this.person.uwregid)
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
      createVisit() {
        if (this.allCreateFieldsSelected) {
          this.createICVisit({
            student_syskey: this.person.system_key,
            program_area: this.checkInData.programArea,
            tutoring_option: this.checkInData.tutoringOption,
            course: this.selectedCourse ? this.selectedCourse.id : null,
            writing_service: this.selectedWritingService
              ? this.selectedWritingService.id
              : null,
          })
            .then(() => {
              this.creatingCheckin = false;
              this.$emit("visit-created");
            })
            .catch((error) => {
              this.createError = error.data;
            });
        }
      },
    },
  };
</script>
