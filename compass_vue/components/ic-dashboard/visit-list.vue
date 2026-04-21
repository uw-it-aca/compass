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
        <td>{{ visit.student_netid }}</td>
        <td>{{ visit.tutoring_option }}</td>
        <td>{{ getCourseString(visit) }}</td>
        <td>{{ getVisitDuration(visit) }}</td>
        <td>{{ getActionString(visit) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>

export default {
  name: "VisitList",
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
    return {
    };
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
  },

};
</script>
