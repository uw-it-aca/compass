<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Resource Eligibility</axdd-card-heading>
    </template>
    <template #body>
      <div v-if="eligibilities.length">
        <div v-for="eligibility in eligibilities">
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
                class="btn btn-sm btn-purple rounded-3 px-3 py-2"
                @click="updateStudentEligibility(eligibility.id)"
              >
                <i class="bi bi-hand-thumbs-up me-1"></i>Approve
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "@/mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {},
  props: {
    person: {
      type: Object,
      required: true,
    },
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
          if (response.data) {
            this.student_eligibilities = response.data;
          }
        }
      );
    },
    loadEligibilities() {
      this.getEligibilities().then((response) => {
        if (response.data) {
          this.eligibilities = response.data;
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
