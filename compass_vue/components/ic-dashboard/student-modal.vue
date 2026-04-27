// student-modal.vue

<template>
  <div v-if="hasLoaded" class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content container">
    <h1> Instructional Center Check In</h1>
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

          <h2>{{ person.full_name }}</h2>
          <p>
            {{ person.student.student_number }}, {{ person.uwnetid }}
            <br />
            {{ person.student.local_phone_number }}
          </p>
        </div>
        <div class="col p-4" v-if="person && !isLoadingVisits && studentVisitData">
          <studenvisitsummary :studentVisits="studentVisitData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getStudentDetail, getStudentVisits } from "@/utils/data";
import StudentVisitSummary from "./student-visit-summary.vue";
import LazyLoad from "@/directives/lazyload";

export default {
  setup() {
    return {
      getStudentDetail,
      getStudentVisits,
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
      errorResponse: null,
      isLoadingStudent: true,
      isLoadingVisits: true,
    };
  },
  computed: {
    hasLoaded() {
      return !this.isLoadingStudent && !this.isLoadingVisits;
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
          }
        })
        .catch((error) => {
          this.errorResponse = error.data;
        })
        .finally(() => {
          this.isLoadingStudent = false;
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
  },
};
</script>
