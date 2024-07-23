<template>
  <div class="p-4" style="background-color: #fafafa; border-radius: 10px">
    <div>
      <h5>Canvas Analytics</h5>
      <i class="bi bi-info-circle-fill me-0"></i>
    </div>
    <div class="d-flex pt-3" style="height: 200px">
      <div class="d-flex justify-content-between w-25">
        <div class="pt-2">
          <ul
            class="p-0 fs-7 text-secondary"
            style="list-style-type: none; line-height: 40px"
          >
            <li>Grade</li>
            <li>Assignment</li>
            <li>Activty</li>
          </ul>
        </div>
        <div class="vr mx-3"></div>
      </div>
      <div class="flex-fill">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </div>
</template>

<script>
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
  name: "App",
  components: {
    Line,
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
            data: [40, 39, 10, 40, 39, 80, 40],
          },
          {
            label: "Assignment",
            backgroundColor: "#4C7286",
            borderColor: "#4C7286",
            data: [30, 29, 6, 30, 49, 60, 30],
          },
          {
            label: "Activity",
            backgroundColor: "#AB9765",
            borderColor: "#AB9765",
            data: [22, 19, 63, 27, 19, 30, 20],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "right",
            labels: {
              usePointStyle: true,
            },
          },
        },
        scales: {
          y: {
            max: 100,
          },
        },
      },
    };
  },
};
</script>
