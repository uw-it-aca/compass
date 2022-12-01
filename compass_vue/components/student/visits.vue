<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2"
        >Instructional Center Visits</axdd-card-heading
      >
    </template>
    <template #body>
      <div>
        <p class="small">
          This student is currently not eligible to use Instructional Center
          resources. <span class="fw-bold">Would you like to grant access?</span>
        </p>
        <div class="text-end">
          <button
            type="button"
            class="btn btn-sm btn-purple rounded-3 px-3 py-2"
            @click="updateEligibility()"
          >
            <i class="bi bi-hand-thumbs-up me-1"></i>Approve
          </button>
        </div>
      </div>

      <div class="d-flex ps-2 mt-4">
        <div class="vr text-muted" aria-hidden="true"></div>
        <ul class="list-unstyled mb-0" style="margin-left: -11px; z-index: 1">
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-purple fs-7 mt-1 me-2 p-1 bg-white"
              ></i>
            </div>
            <div>
              <div>09/23/2020 <strong>BIOL 220</strong></div>
              <div class="text-muted small">10:35am - 11:42am (80min)</div>
            </div>
          </li>
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-purple fs-7 mt-1 me-2 p-1 bg-white"
              ></i>
            </div>
            <div>
              <div>09/23/2020 <strong>BIOL 220</strong></div>
              <div class="text-muted small">10:35am - 11:42am (80min)</div>
            </div>
          </li>
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-purple fs-7 mt-1 me-2 p-1 bg-white"
              ></i>
            </div>
            <div>
              <div>09/23/2020 <strong>BIOL 220</strong></div>
              <div class="text-muted small">10:35am - 11:42am (80min)</div>
            </div>
          </li>
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-purple fs-7 mt-1 me-2 p-1 bg-white"
              ></i>
            </div>
            <div>
              <div>09/23/2020 <strong>BIOL 220</strong></div>
              <div class="text-muted small">10:35am - 11:42am (80min)</div>
            </div>
          </li>
          <li class="d-flex">
            <div>
              <i
                class="bi bi-calendar-check-fill text-purple fs-7 mt-1 me-2 p-1 bg-white"
              ></i>
            </div>
            <div>
              <div>09/23/2020 <strong>BIOL 220</strong></div>
              <div class="text-muted small">10:35am - 11:42am (80min)</div>
            </div>
          </li>
        </ul>
      </div>
    </template>
    <template #footer>Total Visits: 23</template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading } from "axdd-components";

export default {
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
  },
  methods: {
    updateEligibility() {
      alert("please update my eligibility!");
    },
  },
};
</script>
