<template>
  <BCard
    class="shadow-sm rounded-3 mt-3"
    header-class="p-3"
    header-bg-variant="transparent"
  >
    <template #header
      ><div class="fs-6 fw-bold">
        Instructional Center Eligibility
      </div></template
    >

    <div v-if="eligibilities.length">
      <div v-for="(eligibility, index) in eligibilities" :key="index">
        <div v-if="isAssignedEligibility(eligibility)">
          <p class="small">
            This student is eligible to use {{ eligibility.name }}
            resources.
          </p>
        </div>
        <div v-else>
          <p class="small">
            This student is currently not eligible to use
            {{ eligibility.name }}
            resources.
            <span class="fw-bold">Would you like to grant access?</span>
          </p>
          <div class="text-end">
            <button
              type="button"
              class="btn btn-sm btn-outline-primary rounded-3 px-2 py-1"
              @click="updateStudentEligibility(eligibility.id)"
            >
              <i class="bi bi-hand-thumbs-up me-1"></i>Approve
            </button>
          </div>
        </div>
      </div>
    </div>
  </BCard>
</template>

<script>
import { BCard } from "bootstrap-vue-next";

import {
  getEligibilities,
  getStudentEligibility,
  setStudentEligibility,
} from "@/utils/data";

export default {
  name: "StudentEligibility",
  components: { BCard },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      getEligibilities,
      getStudentEligibility,
      setStudentEligibility,
    };
  },
  data() {
    return {
      student_eligibilities: [],
      eligibilities: [],
    };
  },
  created() {
    this.loadStudentEligibilities();
    this.loadEligibilities();
  },
  methods: {
    loadStudentEligibilities() {
      this.getStudentEligibility(this.person.student.system_key).then(
        (response) => {
          if (response) {
            this.student_eligibilities = response;
          }
        }
      );
    },
    loadEligibilities() {
      this.getEligibilities().then((response) => {
        if (response) {
          this.eligibilities = response;
        }
      });
    },
    isAssignedEligibility(eligibility) {
      let is_assigned = false;
      this.student_eligibilities.forEach((item) => {
        if (item.slug == eligibility.slug) is_assigned = true;
      });
      return is_assigned;
    },
    updateStudentEligibility(eligibility_id) {
      this.setStudentEligibility(
        this.person.student.system_key,
        eligibility_id
      ).then(() => {
        this.loadStudentEligibilities();
      });
    },
  },
};
</script>
