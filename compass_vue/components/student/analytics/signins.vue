<template>
  <div class="p-4" style="background-color: #fafafa; border-radius: 10px">
    <div class="d-flex">
      <h5>Sign-In Data</h5>
      <a
        tabindex="0"
        role="button"
        class=""
        data-bs-toggle="popover"
        data-bs-trigger="focus"
        data-bs-placement="top"
        title="Sign-In Data"
        data-bs-content="Sign in data from UW IdP"
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
<!--            Loop over years of signin data we have-->
            <li class="d-flex justify-content-between">
              Winter 2024
              <div>
                 64%
                <i
                  style="color: #c12c2c"
                  class="bi bi-arrow-down-circle-fill ms-2 me-1"
                ></i>
                <i
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
<!--          Loop over quarters of data-->
          <li>
            <i style="color: #4b2e83" class="bi bi-circle-fill me-2"></i>Winter 2024
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
  name: "SignInChart",
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
      rawSigninAnalytics: undefined,
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
        .fetchStudentSigninAnalytics(this.uwnetid)
        .then(() => {
          this.rawSigninAnalytics =
            this.storeAnalytics.signinAnalyticsData[this.uwnetid].data;
        }).catch((e) => {
          this.analyticsNotFound = true;
        });
    },
  }
};
</script>
