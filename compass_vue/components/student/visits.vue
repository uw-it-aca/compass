<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2"
        >Instructional Center Visits</axdd-card-heading
      >
    </template>
    <template #body>
      <!-- TODO: wire this up later when we get the API working -->
      <div v-show="false">
        <p class="small">
          This student is currently not eligible to use Instructional Center
          resources.
          <span class="fw-bold">Would you like to grant access?</span>
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

      <div class="d-flex ps-2">
        <div class="vr text-muted" aria-hidden="true"></div>
        <ul class="list-unstyled mb-0" style="margin-left: -11px; z-index: 1">
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div><strong>BIOL 220</strong> <small>(80min)</small></div>
              <div class="text-muted small">09/23/2020 10:35am - 11:42am</div>
            </div>
          </li>
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div><strong>BIOL 220</strong> <small>(80min)</small></div>
              <div class="text-muted small">09/23/2020 10:35am - 11:42am</div>
            </div>
          </li>
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div><strong>BIOL 220</strong> <small>(80min)</small></div>
              <div class="text-muted small">09/23/2020 10:35am - 11:42am</div>
            </div>
          </li>
          <li class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div><strong>BIOL 220</strong> <small>(80min)</small></div>
              <div class="text-muted small">09/23/2020 10:35am - 11:42am</div>
            </div>
          </li>
          <li class="d-flex">
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div><strong>BIOL 220</strong> <small>(80min)</small></div>
              <div class="text-muted small">09/23/2020 10:35am - 11:42am</div>
            </div>
          </li>
        </ul>
      </div>
    </template>
    <template #footer>Total Visits: 23</template>
  </axdd-card>
</template>

<script>
export default {
  components: {},
  methods: {
    updateEligibility() {
      alert("please update my eligibility!");
    },
  },
};
</script>
