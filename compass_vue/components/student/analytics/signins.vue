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
    <div class="d-flex pt-3" style="height: 225px">
      <div v-if="analyticsNotFound"><p>Analytics data not found</p></div>
      <template v-else>
      <div class="d-flex w-25">
        <div class="pt-2 w-100">
          <ul
            class="p-0 fs-7 text-secondary"
            style="list-style-type: none; line-height: 40px"
          >
            <!-- if score increased compared to last week, arrow up. if score decreased, arrow down. If score did not change, no icons. -->
            <li class="d-flex justify-content-between">
              Grade
              <div>
                {{currentGradeScore}}%
                <i
                  v-if="gradeScoreDecreased"
                  style="color: #c12c2c"
                  class="bi bi-arrow-down-circle-fill ms-2 me-1"
                ></i>
                <i
                  v-else-if="gradeScoreIncreased"
                  style="color: #289026"
                  class="bi bi-arrow-up-circle-fill ms-2 me-1"
                ></i>
              </div>
            </li>

            <li class="d-flex justify-content-between">
              Assignment
              <div>
                {{currentAssignmentScore}}%
                <i
                  v-if="assignmentScoreDecreased"
                  style="color: #c12c2c"
                  class="bi bi-arrow-down-circle-fill ms-2 me-1"
                ></i>
                <i
                  v-else-if="assignmentScoreIncreased"
                  style="color: #289026"
                  class="bi bi-arrow-up-circle-fill ms-2 me-1"
                ></i>
              </div>
            </li>
            <li class="d-flex justify-content-between">
              Activity
              <div>
                {{currentActivityScore}}%
                <i
                  v-if="activityScoreDecreased"
                  style="color: #c12c2c"
                  class="bi bi-arrow-down-circle-fill ms-2 me-1"
                ></i>
                <i
                  v-else-if="activityScoreIncreased"
                  style="color: #289026"
                  class="bi bi-arrow-up-circle-fill ms-2 me-1"
                ></i>
              </div>
            </li>
          </ul>
        </div>
        <div class="vr mx-3"></div>
      </div>
      <div class="flex-fill">
        <Line v-if="dataReady" :data="chartData" :options="chartOptions" />
      </div>
      <div>
        <ul class="p-0 fs-8 text-secondary" style="list-style-type: none">
          <li>
            <i style="color: #4b2e83" class="bi bi-circle-fill me-2"></i>Grade
          </li>
          <li>
            <i style="color: #4c7286" class="bi bi-circle-fill me-2"></i
            >Assignment
          </li>
          <li>
            <i style="color: #ab9765" class="bi bi-circle-fill me-2"></i>Activty
          </li>
        </ul>
      </div>
      </template>
    </div>
  </div>
</template>

<script>
import { Popover } from "bootstrap";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  scales,
} from "chart.js";
import { useAnalyticsStore} from "@/stores/analytics.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  scales
);

export default {
  name: "CanvasAnalyticsChart",
  components: {
    Line,
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
      chartData: {
        labels: ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10"],
        datasets: [
          {
            label: "Grade",
            backgroundColor: "#4B2E83",
            borderColor: "#4B2E83",
            data: [],
          },
          {
            label: "Assignment",
            backgroundColor: "#4C7286",
            borderColor: "#4C7286",
            data: [],
          },
          {
            label: "Activity",
            backgroundColor: "#AB9765",
            borderColor: "#AB9765",
            data: [],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            max: 100,
          },
          x: {
            grid: {
              display: false,
            },
          },
        },
      },
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
      this.setDataForLabel("Grade", this.getDataArrayForKey("grade_score"));
      this.setDataForLabel("Assignment", this.getDataArrayForKey("assignment_score"));
      this.setDataForLabel("Activity", this.getDataArrayForKey("activity_score"));
      this.dataReady = true;
    }
  },
  computed: {
    currentGradeScore() {
      return this.getLatestScore("grade_score");
    },
    currentAssignmentScore() {
      return this.getLatestScore("assignment_score");
    },
    currentActivityScore() {
      return this.getLatestScore("activity_score");
    },
    gradeScoreIncreased() {
      return this.scoreIncreased("grade_score");
    },
    gradeScoreDecreased() {
      return this.scoreDecreased("grade_score");
    },
    assignmentScoreIncreased() {
      return this.scoreIncreased("assignment_score");
    },
    assignmentScoreDecreased() {
      return this.scoreDecreased("assignment_score");
    },
    activityScoreIncreased() {
      return this.scoreIncreased("activity_score");
    },
    activityScoreDecreased() {
      return this.scoreDecreased("activity_score");
    },

  },
  methods: {
    getLatestScore(key) {
      try {
        return this.rawCourseAnalytics[this.rawCourseAnalytics.length - 1][key] * 20;
      } catch (e) {
        return 0;
      }
    },
    scoreIncreased(key) {
      console.log(key)
      try{
        if (this.rawCourseAnalytics.length < 2) {
          console.log('f1')
          return false;
        }

        console.log(this.rawCourseAnalytics[this.rawCourseAnalytics.length - 1][key], this.rawCourseAnalytics[this.rawCourseAnalytics.length - 2][key])
        return this.rawCourseAnalytics[this.rawCourseAnalytics.length - 1][key] >
          this.rawCourseAnalytics[this.rawCourseAnalytics.length - 2][key];
      } catch (e) {
        return false;
      }
    },
    scoreDecreased(key) {
      try{
        if (this.rawCourseAnalytics.length < 2) {
          return false;
        }
        return this.rawCourseAnalytics[this.rawCourseAnalytics.length - 1][key] <
          this.rawCourseAnalytics[this.rawCourseAnalytics.length - 2][key];
      } catch (e) {
        return false;
      }
    },
    setDataForLabel: function(label, data_array){
      for (let dataset of this.chartData.datasets) {
        if (dataset.label == label) {
          dataset.data = data_array;
        }
      }
    },
    getDataArrayForKey(key){
      let data_array = Array(10).fill(null);
      for (let data of this.rawCourseAnalytics) {
        // TODO: Alter multiplier if we change scaling at data generation
        data_array[data.week_id - 1] = data[key] * 20;
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
