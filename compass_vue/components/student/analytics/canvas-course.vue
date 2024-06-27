<template>
  <div class="d-flex border p-1">
    <div class="w-25">
      <h3 class="fs-6">Canvas Analytics</h3>
      <ul>
        <li>Grade</li>
        <li>Assignment</li>
        <li>Activty</li>
      </ul>
    </div>
    <div class="flex-fill">
      <Line :data="chartData" :options="chartOptions" />
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
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: "App",
  components: {
    Line,
  },
  data() {
    return {
      chartData: {
        labels: [
          "W1",
          "W2",
          "W3",
          "W4",
          "W5",
          "W6",
          "W7",
          "W8",
          "W9",
          "W10",
          "W11",
          "W12",
        ],
        datasets: [
          {
            label: "Grade",
            backgroundColor: "purple",
            data: [40, 39, 10, 40, 39, 80, 40],
          },
          {
            label: "Assignment",
            backgroundColor: "gold",
            data: [30, 29, 6, 30, 49, 60, 30],
          },
          {
            label: "Activity",
            backgroundColor: "teal",
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
      },
    };
  },
};
</script>
