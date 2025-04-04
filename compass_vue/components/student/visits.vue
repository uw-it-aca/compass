<template>
  <BCard
    class="shadow-sm rounded-3"
    header-class="p-3"
    header-bg-variant="transparent"
    footer-bg-variant="transparent"
  >
    <template #header>
      <div class="fs-6 fw-bold">Instructional Center Visits</div>
    </template>

    <div v-if="visits.length" class="d-flex ps-2">
      <div class="vr text-muted" aria-hidden="true"></div>
      <ul
        class="list-unstyled mb-0 overflow-auto w-100 flex-fill"
        style="margin-left: -11px; z-index: 1; max-height: 400px"
      >
        <li v-for="(visit, index) in visits" :key="index" class="d-flex mb-3">
          <div>
            <i
              class="bi bi-calendar-check-fill text-body-tertiary fs-7 ms-1 me-3"
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
    <div v-else class="p-3">No visits found</div>

    <template #footer>Total Visits: {{ visits.length }}</template>
  </BCard>
</template>

<script>
import { getStudentVisits } from "@/utils/data";
import {
  formatUTCToLocalDate,
  formatUTCToLocalDateAndTimeZone,
  getMinutesApart,
} from "@/utils/dates.js";

import { BCard } from "bootstrap-vue-next";

export default {
  name: "StudentVisits",
  components: { BCard },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      getStudentVisits,
    };
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
        if (response) {
          this.visits = response;
        }
      });
    },
    visitDuration: function (visit) {
      return getMinutesApart(visit.checkin_date, visit.checkout_date);
    },
    visitDate: function (visit) {
      return formatUTCToLocalDate(visit.checkin_date, "MM/DD/YYYY");
    },
    visitCheckin: function (visit) {
      return formatUTCToLocalDate(visit.checkin_date, "hh:mma");
    },
    visitCheckout: function (visit) {
      return formatUTCToLocalDateAndTimeZone(visit.checkout_date, "hh:mma");
    },
  },
};
</script>
