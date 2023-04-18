<template>
  <div class="bg-dark-purple rounded-3 text-light mb-1 p-3">
    <div class="small">
      <i class="bi bi-calendar-week me-2"></i>
      <span v-if="termData.isBreak">
        <span v-if="termData.breakYear !== termData.year">
          {{ termData.year }} / {{ termData.breakYear }}
        </span>
        <span v-else>{{ termData.year }}</span>
      </span>
      <span v-else class="text-capitalize">
        {{ termData.quarter }}
        {{ termData.year }}
      </span>
    </div>

    <div class="fw-bold">
      <span v-if="termData.isFinals">Finals Week</span>
      <span v-else-if="termData.isBreak" class="text-capitalize">
        {{ termData.breakQuarter }}
        Break
      </span>
      <span v-else class="d-block fw-bold">
        Week {{ getWeeksApart(termData.firstDay, todayDate) }} of
        {{ getWeeksApart(termData.firstDay, termData.lastDay) }}
      </span>
    </div>
    <div class="small mt-3">{{ formatDate(todayDate, "LLLL") }}</div>
  </div>
</template>

<script>
import {
  formatDate,
  getToday,
  getYesterday,
  getWeeksApart,
} from "../../utils/dates";

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
    return {
      todayDate: getToday(),
      yesterdayDate: getYesterday(),
    };
  },
  methods: {},
};
</script>
