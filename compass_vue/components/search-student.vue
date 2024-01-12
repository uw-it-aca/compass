<template>
  <div class="input-group">
    <input
      type="text"
      class="form-control form-control-sm"
      placeholder="Student number or netid..."
      aria-label="Recipient's username"
      v-model="searchValue"
    />
    <button
      :disabled="searchValue.length == 0"
      class="btn btn-sm btn-outline-dark-beige"
      type="button"
      @click="searchByStudent"
    >
      Search
    </button>
  </div>
  <div v-if="!studentExists || error" class="text-danger mt-2">
    No student found
  </div>
</template>

<script>
import { getStudentDetail } from "@/utils/data";

export default {
  props: {
    error: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  setup() {
    return {
      getStudentDetail,
    };
  },
  data() {
    return {
      studentExists: true,
      searchValue: "",
    };
  },
  methods: {
    searchByStudent: function () {
      this.getStudentDetail(this.searchValue)
        .then(() => {
          console.log(this.searchValue);
          this.studentExists = true;
          //this.$router.push("/student/" + this.searchValue);
          window.location.href = "/student/" + this.searchValue;
        })
        .catch(() => {
          this.studentExists = false;
        });
    },
  },
};
</script>
