// student-modal.vue

<template>
  <div :v-if="!isLoading"class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="student-bio p-4" v-if="!isLoading && person">
        <div
          class="rounded-circle border border-light-subtle border-3 mb-3"
        >
          <img
            data-url="/api/internal/photo/9136CCB8F66711D5BE060004AC494FFE/96LV54HIIFUPEZG4/"
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
    </div>
  </div>
</template>

<script>
import { getStudentDetail } from "@/utils/data";

export default {
  setup() {
    return {
      getStudentDetail,
    };
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
      errorResponse: null,
      isLoading: true,
    };
  },
  computed: {},
  mounted() {
    this.loadStudent();
  },
  methods: {
    loadStudent: function () {
      // setup() exposed properties can be accessed on `this`
      this.getStudentDetail(this.studentIdentifier)
        .then((response) => {
          if (response) {
            this.person = response;
            console.log("Student data loaded successfully", response);
            this.errorResponse = null;
          }
        })
        .catch((error) => {
          this.errorResponse = error.data;
        })
        .finally(() => {
          this.isLoading = false;
          console.log('done ')
        });
    },
  },
};
</script>
