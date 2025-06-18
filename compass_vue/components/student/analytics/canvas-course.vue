<template>
  <div class="m-3 mt-0 p-3 bg-body-tertiary rounded-3">
    <div class="d-flex">
      <div class="text-uppercase text-dark-beige fs-8 fw-bold mb-3">
        Canvas Analytics
      </div>
      <a
        tabindex="0"
        role="button"
        class=""
        data-bs-toggle="popover"
        data-bs-trigger="focus"
        data-bs-placement="top"
        title="Canvas Analytics"
        data-bs-content="Grade represents the student’s grade in Canvas relative to her classmates up to this point in the quarter. Assignment is indicative of how the student is doing relative to her classmates with regards to the status of assignments. "
      >
        <i class="bi bi-info-circle-fill ms-2"></i>
      </a>
    </div>
    <div v-if="analyticsNotFound">Course analytics not found.</div>
    <template v-else>
      <AnalyticsChart
        v-if="dataReady"
        :data-series="formattedSeriesData"
        :show-only-latest="false"
      ></AnalyticsChart>
    </template>
  </div>
</template>

<script>
import { Popover } from "bootstrap";
import { useAnalyticsStore } from "@/stores/analytics.js";
import AnalyticsChart from "@/components/student/analytics/chart.vue";

export default {
  name: "CanvasAnalyticsChart",
  components: {
    AnalyticsChart,
  },

  props: {
    uwnetid: {
      type: String,
      required: true,
    },
    year: {
      type: Number,
      required: true,
    },
    quarter: {
      type: String,
      required: true,
    },
    courseId: {
      type: String,
      required: true,
    },
  },
  setup() {
    const storeAnalytics = useAnalyticsStore();
    return { storeAnalytics };
  },
  data() {
    return {
      rawCourseAnalytics: undefined,
      analyticsNotFound: false,
      dataReady: false,
    };
  },
  computed: {
    formattedSeriesData() {
      return [
        {
          label: "Grade",
          data: this.getDataArrayForKey("grade_score"),
          backgroundColor: "#4B2E83",
          borderColor: "#4B2E83",
        },
        {
          label: "Assignment",
          data: this.getDataArrayForKey("assignment_score"),
          backgroundColor: "#4C7286",
          borderColor: "#4C7286",
        },
        {
          label: "Activity",
          data: this.getDataArrayForKey("activity_score"),
          backgroundColor: "#AB9765",
          borderColor: "#AB9765",
        },
      ];
    },
  },
  watch: {
    rawCourseAnalytics: function () {
      this.dataReady = true;
    },
  },
  mounted() {
    // enable popovers everywhere
    // https://getbootstrap.com/docs/5.1/components/popovers/#example-enable-popovers-everywhere
    var popoverTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
      return new Popover(popoverTriggerEl);
    });

    this.loadStudentCourseAnalytics();
  },
  methods: {
    getDataArrayForKey(key) {
      let data_array = Array(10).fill(null);
      for (let data of this.rawCourseAnalytics) {
        data_array[data.week_id - 1] = data[key];
      }
      return data_array;
    },
    loadStudentCourseAnalytics: function () {
      this.storeAnalytics
        .fetchStudentCourseAnalytics(
          this.uwnetid,
          this.year,
          this.quarter,
          this.course_id
        )
        .then(() => {
          this.rawCourseAnalytics =
            this.storeAnalytics.courseAnalyticsData[this.uwnetid][this.year][
              this.quarter
            ][this.course_id].data;
        })
        .catch((e) => {
          this.analyticsNotFound = true;
        });
    },
  },
};
</script>
