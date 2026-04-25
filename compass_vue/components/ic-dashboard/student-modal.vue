// student-modal.vue

<template>
  <div :v-if="!isLoading" class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="student-bio p-4" v-if="!isLoading && person">
        <div
          v-lazyload
          class="mb-3"
        >
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
    </div>
  </div>
</template>

<script>
import { getStudentDetail } from "@/utils/data";
import LazyLoad from "@/directives/lazyload";

export default {
  setup() {
    return {
      getStudentDetail,
    };
  },
  directives: {
    lazyload: LazyLoad,
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
            this.errorResponse = null;
          }
        })
        .catch((error) => {
          this.errorResponse = error.data;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
};
</script>
