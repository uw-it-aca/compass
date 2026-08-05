// visit-list.vue

<template>
  <h2>{{ listTitle }}</h2>
  <table>
    <thead>
      <tr>
        <th>Student</th>
        <th>Type</th>
        <th>Course</th>
        <th>Time</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="visit in visits" :key="visit.id">
        <td>
          <template v-if="visit.student">
            <profile-mini :person="visit.student"></profile-mini>
          </template>
          <template v-else> Student data not found </template>
        </td>
        <td>{{ visit.tutoring_option }}</td>
        <td>{{ getCourseString(visit) }}</td>
        <td>{{ getVisitDuration(visit) }}</td>
        <td v-if="!visit.is_verified">
          <button @click="verifyVisit(visit.id)">Verify</button>
        </td>
        <td v-else>
          <button @click="checkOutVisit(visit.id)">Check Out</button>
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
