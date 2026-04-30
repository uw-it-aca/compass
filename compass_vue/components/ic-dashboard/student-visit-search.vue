// student-visit-search.vue

<template>
  <p>Search all students:</p>
  <form onsubmit="return false;">
    <div class="input-group">
      <input
        v-model="searchValue"
        type="text"
        :maxlength="maxLength"
        class="form-control form-control-sm"
        placeholder="Student number or UW netid..."
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
    </div>
  </form>

  <div
    id="studentSearchModal"
    ref="studentSearchModal"
    class="modal fade"
    tabindex="-1"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered">
      <div class="modal-content container">
        <h1>Instructional Center Check In</h1>
        <div v-if="!validQuery">Invalid student identifier</div>
        <div v-else class="row">
          <!-- left column -->
          <div v-if="searchError" class="alert alert-danger col">
            Could not find a student matching "{{ searchValue }}". Please try
            again.
          </div>
          <div v-else-if="person" class="student-bio col p-4">
            <div v-lazyload class="mb-3">
              <img
                :data-url="person.photo_url"
                :alt="person.display_name + ' profile picture'"
                class="img-profile rounded-circle border border-3"
                @error="
                  $event.target.src = '/static/compass/img/placeholder.png'
                "
              />
            </div>
            <span v-if="isICEligible">IC Eligible</span>
            <span v-else>Not Eligible</span>
            <h2>{{ person.full_name }}</h2>
            <p>
              {{ person.student.student_number }}, {{ person.uwnetid }}
              <br />
              {{ person.student.local_phone_number }}
            </p>
          </div>
          <!-- right column -->
          <div v-if="rightColHasData" class="col">
            <div v-if="displayMode === 'visits'">
              <studenvisitsummary :studentVisits="studentVisitData" />
            </div>
            <div v-else-if="displayMode === 'not_eligible'">
              This student is not eligible for IC visits.
              <button class="btn btn-primary ms-3" @click="addICEligibility()">
                Approve
              </button>
            </div>
            <div v-else-if="displayMode === 'checkin'">Checking in...</div>
          </div>

          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button
            v-if="showCheckinButton"
            class="btn btn-primary ms-2"
            @click="setCheckinMode()"
          >
            Check In
          </button>
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
          (eligibility) => eligibility.slug === window.icVisitsEligibilitySlug,
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
      this.creatingCheckin = true;
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
  },
};
</script>
