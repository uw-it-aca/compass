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

      <div v-if="visits.length" class="d-flex ps-2">
        <div class="vr text-muted" aria-hidden="true"></div>
        <ul class="list-unstyled mb-0" style="margin-left: -11px; z-index: 1">
          <li
            v-for="visit in visits"
            class="d-flex mb-3"
          >
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div><strong>{{ visit.course_code }}</strong> <small>({{ visitDuration(visit) }}min)</small></div>
              <div class="text-muted small">{{ visitDate(visit) }} {{ visitCheckin(visit) }} - {{ visitCheckout(visit) }}</div>
            </div>
          </li>
        </ul>
      </div>
    </template>
    <template #footer>Total Visits: {{ visits.length }}</template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";

export default {
  mixins: [dataMixin],
  components: {},
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      visits: [],
    };
  },
  created() {
    this.loadStudentVisits();
  },
  methods: {
    loadStudentVisits: function () {
      this.getStudentVisits(this.person.student.system_key).then(
        (response) => {
          if (response.data) {
            this.visits = response.data;
          }
        }
      );
    },
    visitDuration: function (visit) {
      var checkin = new Date(visit.checkin_date), checkout = new Date(visit.checkout_date);
      return Math.abs(Math.round((checkout.getTime() - checkin.getTime()) / 1000 / 60));
    },
    visitDate: function (visit) {
      var checkin = new Date(visit.checkin_date);
      return this.dateMMDDYYYY(checkin);
    },
    visitCheckin: function (visit) {
      var checkin = new Date(visit.checkin_date);
      return this.dateHHMMampm(checkin);
    },
    visitCheckout: function (visit) {
      var checkout = new Date(visit.checkout_date);
      return this.dateHHMMampm(checkout);
    },
    updateEligibility() {
      alert("please update my eligibility!");
    },
  },
};
</script>
