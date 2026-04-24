// student-visit-search.vue

<template>
  <p>Search all students:</p>
  <form @submit.prevent="searchByStudent">
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
        :disabled="searchValue.length == 0"
        class="btn btn-sm btn-outline-primary"
        type="submit"
      >
        Search
      </button>
    </div>
    <div v-if="searchError" class="text-danger mt-2">
      {{ searchError.message }}
    </div>
  </form>
  <studentmodal v-if="showModal" :student-identifier="modalPersonId" />
</template>

<script>
import { useICVisitsStore } from "@/stores/ic-visits";
import { getStudentBySearch } from "@/utils/data";
import StudentModal from "@/components/ic-dashboard/student-modal.vue";

export default {
  setup: function () {
    return {
      getStudentBySearch,
    };
  },
  name: "StudentVisitSearch",
  components: {
    studentmodal: StudentModal,
  },
  data() {
    return {
      icVisitsStore: useICVisitsStore(),
      searchValue: "javerage",
      maxLength: 32,
      searchError: null,
      showModal: false,
      studentProfileData: null,
      modalPersonId: null,
    };
  },
  computed: {
    studentVisitData() {
      return this.icVisitsStore.getStudentVisitData(this.searchValue);
    },
  },
  methods: {
    validQuery: function (val) {
      return val.length < 2 ||
        val.length > this.maxLength ||
        !/^[a-z0-9\-\_\.]+$/.test(val)
        ? false
        : true;
    },
    searchByStudent: function () {
      this.searchError = null;
      this.searchValue = this.searchValue.trim().toLowerCase();
      if (this.validQuery(this.searchValue)) {
        this.getStudentBySearch(this.searchValue)
          .then((response) => {
            this.showModal = true;
            this.modalPersonId = this.searchValue;
          })
          .catch((err) => {
            this.searchError = { message: "Error fetching student data" };
            console.error("Error fetching student data", err);
            this.modalPersonId = null;
          });

        // this.icVisitsStore.fetchStudentVisit(this.searchValue).then((req) => {
        //   console.log('Student visit data fetched successfully', this.icVisitsStore.getStudentVisitData(this.searchValue));
        //   // TODO: Fire off modal init here
        //   this.showModal = true;
        // }).catch((err) => {
        //   this.searchError = { message: "Error fetching student visit data" };
        //   console.error('Error fetching student visit data', err);
        // });
      } else {
        this.searchError = { message: "Invalid student identifier" };
      }
    },
  },
};
</script>
