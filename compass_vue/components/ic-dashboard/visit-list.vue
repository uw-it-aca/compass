// visit-list.vue

<template>
  <h2 class="fs-3 fw-light ff-encode-sans py-2 mt-4">{{ listTitle }}</h2>
  <table class="table table-striped">
    <colgroup>
      <col style="width: 30%">
      <col style="width: 22.5%">
      <col style="width: 22.5%">
      <col style="width: 15%">
      <col style="width: 10%">
    </colgroup>
    <thead class="table-light">
      <tr>
        <th class="ps-4">Student</th>
        <th>Type</th>
        <th>Course</th>
        <th>Time</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-if="visits.length === 0">
        <td colspan="6" class="text-center text-muted py-4">
          No students in this category.
        </td>
      </tr>
      <tr v-for="visit in visits" :key="visit.id">
        <td class="ps-4">
          <template v-if="visit.student">
            <profile-mini :person="visit.student"></profile-mini>
          </template>
          <template v-else> Student data not found </template>
        </td>
        <td>{{ visit.tutoring_option }}</td>
        <td>{{ getCourseString(visit) }}</td>
        <td>{{ getVisitDuration(visit) }}</td>
        <td v-if="!visit.is_verified">
          <button
            class="btn btn-outline-primary btn-sm" type="button"
            @click="verifyVisit(visit.id)"
            >Verify
          </button>
        </td>
        <td v-else>
          <button
            class="btn btn-outline-primary btn-sm" type="button"
            @click="checkOutVisit(visit.id)"
            >Check Out
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { updateICVisit } from "@/utils/data";
import ProfileMini from "@/components/student/profile-mini.vue";

export default {
  name: "VisitList",
  components: {
    ProfileMini,
  },
  setup: function () {
    return {
      updateICVisit,
    };
  },
  props: {
    visits: {
      type: Array,
      required: true,
    },
    listTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {};
  },
  methods: {
    getCourseString(visit) {
      if (visit.writing_service) {
        return visit.writing_service;
      } else {
        return visit.course;
      }
    },
    getVisitDuration(visit) {
      // elapsed time since visit check_in_date
      const checkInTime = new Date(visit.check_in_date);
      const now = new Date();
      const elapsedTime = now - checkInTime;
      const minutes = Math.floor(elapsedTime / 60000);
      return `${minutes} min`;
    },
    getActionString(visit) {
      if (!visit.is_verified) {
        return "Verify";
      } else {
        return "Check Out";
      }
    },
    checkOutVisit(visit_id) {
      this.updateICVisit(visit_id, {
        is_checked_out: true,
      }).then(() => {
        this.$emit("visit-updated");
      });
    },
    verifyVisit(visit_id) {
      this.updateICVisit(visit_id, {
        is_verified: true,
      }).then(() => {
        this.$emit("visit-updated");
      });
    },
  },
};
</script>

<style scoped>
.visit-table {
  table-layout: fixed;
}
</style>
