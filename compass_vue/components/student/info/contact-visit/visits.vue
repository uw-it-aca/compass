<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2"
        >Instructional Center Visits</axdd-card-heading
      >
    </template>
    <template #body>
      <div v-if="visits.length" class="d-flex ps-2">
        <div class="vr text-muted" aria-hidden="true"></div>
        <ul
          class="list-unstyled mb-0 overflow-auto w-100 flex-fill"
          style="margin-left: -11px; z-index: 1; max-height: 400px"
        >
          <li v-for="(visit, index) in visits" :key="index" class="d-flex mb-3">
            <div>
              <i
                class="bi bi-calendar-check-fill text-gray fs-7 ms-1 me-3 bg-white"
              ></i>
            </div>
            <div>
              <div>
                <strong>{{ visit.course_code }}</strong>
                <small>({{ visitDuration(visit) }}min)</small>
              </div>
              <div class="text-muted small">
                {{ visitDate(visit) }} {{ visitCheckin(visit) }} -
                {{ visitCheckout(visit) }}
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div v-else class="text-muted">No visits found</div>
    </template>
    <template #footer>Total Visits: {{ visits.length }}</template>
  </axdd-card>
</template>

<script>
import dataMixin from "@/mixins/data_mixin.js";
import { formatDate, getMinutesApart } from "@/utils/dates.js";

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
      this.getStudentVisits(this.person.student.system_key).then((response) => {
        if (response.data) {
          this.visits = response.data;
        }
      });
    },
    visitDuration: function (visit) {
      return getMinutesApart(visit.checkin_date, visit.checkout_date);
    },
    visitDate: function (visit) {
      return formatDate(visit.checkin_date, "MM/DD/YYYY");
    },
    visitCheckin: function (visit) {
      return formatDate(visit.checkin_date, "hh:mma");
    },
    visitCheckout: function (visit) {
      return formatDate(visit.checkout_date, "hh:mma");
    },
  },
};
</script>
