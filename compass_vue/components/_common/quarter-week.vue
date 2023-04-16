<template>
  <div class="my-auto">
    <div class="text-secondary text-end small">
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

    <div class="text-end fw-bold">
      <span v-if="termData.isFinals">Finals Week</span>
      <span v-else-if="termData.isBreak" class="text-capitalize">
        {{ termData.breakQuarter }}
        Break
      </span>
      <span v-else class="text-dark d-block fw-bold">
        Week {{ getWeeksApart(termData.firstDay, todayDate) }} of
        {{ getWeeksApart(termData.firstDay, termData.lastDay) }}
      </span>
    </div>
    <div class="text-end small text-muted">
      {{ formatDates(todayDate, "LLLL") }}
    </div>
  </div>
</template>

<script>
import dayjs from "dayjs";
import localizedFormat from "dayjs/plugin/localizedFormat";
dayjs.extend(localizedFormat);

export default {
  props: {
    termData: {
      type: Object,
    },
  },
  data() {
    return {
      todayDate: dayjs(),
    };
  },
  methods: {
    getWeeksApart(quarterStartDate, compareDate) {
      const days = dayjs(compareDate).diff(
        dayjs(quarterStartDate).startOf("week"),
        "days"
      );
      if (days < 0) {
        return 0;
      } else {
        return parseInt(days / 7) + 1;
      }
    },
    formatDates(date, format) {
      if (!date) {
        return null;
      }
      return dayjs(date).format(format);
    },
  },
};
</script>
