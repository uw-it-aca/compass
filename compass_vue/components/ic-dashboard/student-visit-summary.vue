// student-visit-summary.vue

<template>
  <div v-if="studentVisits" class="d-flex flex-column h-100 pt-3">
    <div
      v-for="(summary, course) in getVisitSummaryByCourseCode()"
      :key="course"
      class="d-flex flex-row mb-3"
    >
      <p class="fw-semibold me-auto">{{ course }}:</p>
      <div class="d-flex flex-row ms-auto">
        <p class="fw-semibold me-2">{{ summary.count }}</p>
        <p class="me-2">
          {{ summary.count === 1 ? "visit" : "visits" }}
        </p>
        <p class="fw-semibold me-2">{{ Math.round(summary.time) }}</p>
        <p class="me-2">min</p>
      </div>
    </div>

    <div class="d-flex flex-row mt-auto">
      <p class="fw-semibold lead me-auto">Total:</p>
      <div class="d-flex flex-row ms-auto align-items-baseline">
        <p class="fw-semibold lead me-2">
          {{ studentVisits.length }}
        </p>
        <p class="me-2">visit{{ studentVisits.length === 1 ? "" : "s" }}</p>
        <p class="fw-semibold lead me-2">
          {{ Math.round(totalVisitTime) }}
        </p>
        <p class="me-2">min</p>
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

<style lang="scss" scoped>
  .img-profile {
    height: 120px;
    width: 120px;
    object-fit: cover;
    object-position: top;
  }
</style>
