<template>
  <div class="bg-dark-purple rounded-3 text-light mb-1 p-3">
    <div class="small">
      <i class="bi bi-calendar-week me-2"></i>
      <span v-if="termData.isBreak">
        <span v-if="termData.breakYear !== termData.currYear">
          {{ termData.currYear }} / {{ termData.breakYear }}
        </span>
        <span v-else>{{ termData.currYear }}</span>
      </span>
      <span v-else class="text-capitalize">
        {{ termData.currQuarter }}
        {{ termData.currYear }}
      </span>
    </div>

    <div class="fw-bold">
      <span v-if="termData.isFinals">Finals Week</span>
      <span v-else-if="termData.isBreak" class="text-capitalize">
        {{ termData.breakQuarter }}
        Break
      </span>
      <span v-else class="d-inline-block fw-bold">
        Week {{ termData.weekOfTerm }} of
        {{ getWeeksApart(termData.firstDay, termData.lastDay) }}
      </span>
    </div>
    <div class="small mt-3">{{ formatDate(termData.todayDate, "LLLL") }}</div>
  </div>
</template>

<script>
import { formatDate, getWeeksApart } from "../../utils/dates";

export default {
  props: {
    termData: {
      type: Object,
    },
  },
  setup() {
    // setup is used for composition api
    return {
      formatDate,
      getWeeksApart,
    };
  },
  data() {
    return {};
  },
  methods: {},
};
</script>
