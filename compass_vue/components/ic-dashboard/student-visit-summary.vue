// student-visit-summary.vue

<template>
  <div>
    <div v-if="studentVisits">
        <div
          v-for="(summary, course) in getVisitSummaryByCourseCode()"
          :key="course"
        >
          {{ course }}: {{ summary.count }} visit{{ summary.count === 1 ? '' : 's' }} {{ Math.round(summary.time) }} minutes
        </div>
      <div>
        Total: {{ studentVisits.length }} visit{{ studentVisits.length === 1 ? '' : 's' }} {{ Math.round(totalVisitTime) }} minutes
      </div>

    </div>
  </div>
</template>

<script>

export default {
  name: "StudentVisitSummary",
  props: {
    studentVisits: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {};
  },
  computed: {
    totalVisitTime() {
      return this.studentVisits.reduce((total, visit) => {
        const checkinTime = new Date(visit.checkin_date);
        const checkoutTime = new Date(visit.checkout_date);
        const visitDuration = (checkoutTime - checkinTime) / 60000; // duration in minutes
        return total + visitDuration;
      }, 0);
    },
  },
  mounted() {},
  methods: {
      getVisitSummaryByCourseCode() {
        const summaryByCourse = {};
        this.studentVisits.forEach((visit) => {
          const courseCode = visit.course_code || "Unknown Course";
          const checkinTime = new Date(visit.checkin_date);
          const checkoutTime = new Date(visit.checkout_date);
          const visitDuration = (checkoutTime - checkinTime) / 60000; // duration in minutes
          if (!summaryByCourse[courseCode]) {
            summaryByCourse[courseCode] = { count: 0, time: 0 };
          }
          summaryByCourse[courseCode].count += 1;
          summaryByCourse[courseCode].time += visitDuration;
        });
        return summaryByCourse;
      },
  },
};
</script>
