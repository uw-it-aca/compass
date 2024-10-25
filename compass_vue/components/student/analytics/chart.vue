<template>
  <div class="d-flex" >
    <div class="d-flex w-25">
      <div class="pt-2 w-100">
        <ul
          class="p-0 fs-7 text-body-secondary"
        >
          <template v-for="(dataset, index) in dataSeries" :key="index">
            <li
              class="d-flex justify-content-between"
              v-if="displayLatestValue(dataset)"
            >
              {{ dataset.label }}
              <div>
                {{ getLatestScore(dataset.data) }}%
                <i
                  v-if="latestScoreDecreased(dataset.data)"
                  class="bi bi-arrow-down-circle-fill text-danger ms-2 me-1"
                ></i>
                <i
                  v-else-if="latestScoreIncreased(dataset.data)"
                  class="bi bi-arrow-up-circle-fill text-success ms-2 me-1"
                ></i>
                <i v-else class="bi bi-circle  ms-2 me-1 opacity-0" aria-hidden="true"></i>
              </div>
            </li>
          </template>
        </ul>
      </div>
      <div class="vr mx-3"></div>
    </div>
    <div class="flex-fill">
      <Line v-if="showChart" :data="chartData" :options="chartOptions" />
    </div>
    <div>
      <ul class="p-0 fs-8 text-body-secondary" style="list-style-type: none">
        <li v-for="(dataset, index) in dataSeries" :key="index">
          <i
            :style="{ color: dataset.backgroundColor }"
            class="bi bi-circle-fill me-2"
          ></i
          >{{ dataset.label }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
//import { Popover } from "bootstrap";
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
  name: "AnalyticsChart",
  components: {
    // eslint-disable-next-line vue/no-reserved-component-names
    Line,
  },
  setup() {},
  props: {
    dataSeries: {
      type: Array,
      required: true,
    },
    showOnlyLatest: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  data() {
    return {
      chartData: {
        labels: ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10"],
        datasets: [],
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
      rawCourseAnalytics: [],
      showChart: false,
    };
  },
  mounted() {
    this.chartData.datasets = this.dataSeries;
    this.showChart = true;
  },
  methods: {
    displayLatestValue(dataset) {
      if (this.showOnlyLatest) {
        return dataset.isLatest;
      }
      return true;
    },
    getLatestScore(dataset) {
      let latest_value = null;
      for (let data of dataset) {
        if (data !== null) {
          latest_value = data;
        }
      }
      return latest_value;
    },
    getLatestScoreIndex(dataset) {
      let latest_idx;
      for (let i = dataset.length - 1; i >= 0; i--) {
        if (dataset[i] !== null) {
          latest_idx = i;
          break;
        }
      }
      return latest_idx;
    },
    latestScoreIncreased(dataset) {
      let latest_idx = this.getLatestScoreIndex(dataset);
      if (latest_idx === 0) {
        return false;
      } else {
        return dataset[latest_idx] > dataset[latest_idx - 1];
      }
    },
    latestScoreDecreased(dataset) {
      let latest_idx = this.getLatestScoreIndex(dataset);
      if (latest_idx === 0) {
        return false;
      } else {
        return dataset[latest_idx] < dataset[latest_idx - 1];
      }
    },
  },
};
</script>
