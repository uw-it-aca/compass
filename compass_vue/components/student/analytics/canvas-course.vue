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
      <div class="d-flex w-25">
        <div class="pt-2 w-100">
          <ul
            class="p-0 fs-7 text-secondary"
            style="list-style-type: none; line-height: 40px"
          >
            <!-- if score increased compared to last week, arrow up. if score decreased, arrow down. If score did not change, no icons. -->
            <li>
              <div class="d-flex justify-content-between">
                Grade
                <div>
                  40%
                  <i
                    style="color: #c12c2c"
                    class="bi bi-arrow-down-circle-fill ms-2 me-1"
                  ></i>
                  <i
                    style="color: #289026"
                    class="bi bi-arrow-up-circle-fill ms-2 me-1"
                  ></i>
                </div>
              </div>
            </li>

            <li>
              <div class="d-flex justify-content-between">
                Assignment
                <div>
                  30%
                  <i
                    style="color: #c12c2c"
                    class="bi bi-arrow-down-circle-fill ms-2 me-1"
                  ></i>
                  <i
                    style="color: #289026"
                    class="bi bi-arrow-up-circle-fill ms-2 me-1"
                  ></i>
                </div>
              </div>
            </li>
            <li>
              <div class="d-flex justify-content-between">
                Activity
                <div>
                  20%
                  <i
                    style="color: #c12c2c"
                    class="bi bi-arrow-down-circle-fill ms-2 me-1"
                  ></i>
                  <i
                    style="color: #289026"
                    class="bi bi-arrow-up-circle-fill ms-2 me-1"
                  ></i>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <div class="vr mx-3"></div>
      </div>
      <div class="flex-fill">
        <Line :data="chartData" :options="chartOptions" />
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
    };
  },
};
</script>
