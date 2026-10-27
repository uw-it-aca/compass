// student-visit-summary.vue

<template>
  <div v-if="studentVisits">
    <div class="card border-0 bg-body-tertiary rounded-3 p-3 mb-">
      <h3 class="fs-6 fw-normal">Total:</h3>
      <p class="fs-1 fw-bold m-0 text-end">
        {{ Math.round(totalVisitTime) }}
        <span class="fs-6 fw-normal text-body-secondary"> mins </span>
        <span class="fs-5 fw-semibold ms-2"> {{ studentVisits.length }} </span>
        <span class="fs-6 fw-normal text-body-secondary"> visits </span>
      </p>
    </div>

    <div class="row row-cols-2 g-2">
      <div
        v-for="(summary, course) in getVisitSummaryByCourseCode()"
        :key="course"
        class="col"
      >
        <div class="card border-0 bg-body-tertiary rounded-3 p-3">
          <h3 class="fs-6 fw-normal">{{ course }}:</h3>
          <p class="fs-5 fw-semibold m-0 text-end">
            {{ Math.round(summary.time) }}
            <span class="fs-6 fw-normal text-body-secondary"> mins </span>
          </p>
        </div>
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
