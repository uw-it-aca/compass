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
/* sample studentVisits data:
[ { "id": 1, "student": 2, "visit_type": { "id": 4, "access_group": { "id": 1, "name": "OMAD", "access_group_id": "u_astra_group1" }, "name": "IC-Tutoring (Drop-In)", "slug": "ic-tutoring-drop-in", "editable": false }, "tutoring_option": null, "course_code": "ESS 203", "checkin_date": "2023-05-26T18:45:00Z", "checkout_date": "2023-05-26T19:17:00Z" }, { "id": 2, "student": 2, "visit_type": { "id": 2, "access_group": { "id": 1, "name": "OMAD", "access_group_id": "u_astra_group1" }, "name": "IC-Exam Prep (Drop-In)", "slug": "ic-exam-prep-drop-in", "editable": false }, "tutoring_option": null, "course_code": "MATH 123", "checkin_date": "2022-11-06T14:22:00Z", "checkout_date": "2022-11-06T15:34:00Z" } ]
*/

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
