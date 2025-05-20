<template>
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
        class="btn btn-sm btn-outline-dark-beige"
        type="submit"
      >
        Search
      </button>
    </div>
    <div v-if="searchError || error" class="text-danger mt-2">
      {{ searchError || "Student not found" }}
    </div>
  </form>
</template>

<script>
import { getStudentBySearch } from "@/utils/data";

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
      getStudentBySearch,
    };
  },
  data() {
    return {
      searchValue: "",
      maxLength: 32,
      searchError: null,
    };
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
            this.$router.push({
              name: "student",
              params: { id: this.searchValue },
            });
          })
          .catch((error) => {
            this.searchError = error;
          });
      } else {
        this.searchError = "Invalid student identifier";
      }
    },
  },
};
</script>
