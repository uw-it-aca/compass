// student-modal.vue

<template>
  <div v-if="hasLoaded" class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content container">
      <h1>Instructional Center Check In</h1>
      <div class="row">
        <div class="student-bio col p-4" v-if="person">
          <div v-lazyload class="mb-3">
            <img
              :data-url="person.photo_url"
              :alt="person.display_name + ' profile picture'"
              class="img-profile rounded-circle border border-3"
              @error="$event.target.src = '/static/compass/img/placeholder.png'"
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
        <div class="col">
          <div v-if="showVisits">
            <studenvisitsummary :studentVisits="studentVisitData" />
          </div>
          <div v-else>
            <div :v-if="!ICEligible">
              This student is not eligible for IC visits.
              <button class="btn btn-primary ms-3" @click="addICEligibility()">
                Approve
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  getStudentDetail,
  getStudentVisits,
  getStudentEligibility,
  setStudentEligibility,
  getEligibilities,
} from "@/utils/data";
import StudentVisitSummary from "./student-visit-summary.vue";
import LazyLoad from "@/directives/lazyload";

export default {
  setup() {
    return {
      getStudentDetail,
      getStudentVisits,
      getStudentEligibility,
      setStudentEligibility,
      getEligibilities,
    };
  },
  directives: {
    lazyload: LazyLoad,
  },
  components: {
    studenvisitsummary: StudentVisitSummary,
  },
  name: "StudentModal",
  props: {
    studentIdentifier: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      person: null,
      studentVisitData: null,
      studentEligibility: null,
      errorResponse: null,
      isLoadingStudent: true,
      isLoadingVisits: true,
      isLoadingEligibility: true,
    };
  },
  computed: {
    hasLoaded() {
      return (
        !this.isLoadingStudent &&
        !this.isLoadingVisits &&
        !this.isLoadingEligibility
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
  },
  mounted() {
    this.loadStudent();
  },
  methods: {
    loadStudent: function () {
      this.getStudentDetail(this.studentIdentifier)
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
          }
        })
        .catch((error) => {
          this.errorResponse = error.data;
        })
        .finally(() => {
          this.isLoadingEligibility = false;
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
