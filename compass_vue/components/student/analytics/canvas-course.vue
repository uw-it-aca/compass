<template>
  <div class="p-4" style="background-color: #fafafa; border-radius: 10px">
    <div class="d-flex">
      <h5>Canvas Analytics</h5>
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
    <template v-if="analyticsNotFound">
      <p>Course analytics not found</p>
    </template>
    <template v-else>
      <analytics-chart v-if="dataReady" :data-series="formattedSeriesData" :show-only-latest="false"></analytics-chart>
    </template>
  </div>
</template>

<script>
import { Popover } from "bootstrap";
import { useAnalyticsStore} from "@/stores/analytics.js";
import AnalyticsChart from "@/components/student/analytics/chart.vue";

export default {
  name: "CanvasAnalyticsChart",
  components: {
    AnalyticsChart
  },
  setup() {
    const storeAnalytics = useAnalyticsStore();
    return { storeAnalytics };
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
    course_id: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      rawCourseAnalytics: undefined,
      analyticsNotFound: false,
      dataReady: false,
    };
  },
  mounted() {
    this.loadStudentCourseAnalytics();
  },
  watch: {
    rawCourseAnalytics: function () {
      this.dataReady = true;
    }
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
        }
      ]
    },
  },
  methods: {
    getDataArrayForKey(key){
      let data_array = Array(10).fill(null);
      for (let data of this.rawCourseAnalytics) {
        data_array[data.week_id - 1] = data[key];
      }
      return data_array;
    },
    loadStudentCourseAnalytics: function () {
      this.storeAnalytics
        .fetchStudentCourseAnalytics(this.uwnetid, this.year, this.quarter, this.course_id)
        .then(() => {
          this.rawCourseAnalytics =
            this.storeAnalytics.courseAnalyticsData[this.uwnetid][this.year][this.quarter][this.course_id].data;
        }).catch((e) => {
          this.analyticsNotFound = true;
        });
    },
  }
};
</script>
