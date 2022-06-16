<template>
  <axdd-card>
    <template #heading>
      <axdd-card-heading :level="2">Schedule (sws)</axdd-card-heading>
    </template>
    <template #body>
      <axdd-tabs :tabs-id="'schedule'">
        <template #items>
          <axdd-tab-item
            v-for="(schedule, index) in schedules"
            :key="index"
            :tabs-id="'schedule'"
            :panel-id="'panel' + index"
            :active-tab="index == 0"
            >{{ schedule.term.quarter }} {{ schedule.term.year }}</axdd-tab-item
          >
        </template>
        <template #panels>
          <template v-if="Object.keys(schedules).length">
            <axdd-tab-panel
              v-for="(schedule, scheduleIndex) in schedules"
              :key="scheduleIndex"
              :panel-id="'panel' + scheduleIndex"
              :active-panel="scheduleIndex == 0"
            >
              <table class="table table-hover table-striped m-0 mb-5">
                <thead class="small">
                  <tr>
                    <th>Course</th>
                    <th>Course Number</th>
                    <th>Credits</th>
                    <th>Grade</th>
                  </tr>
                </thead>
                <tbody class="mb-3">
                  <tr
                    v-for="(section, index) in schedule.sections"
                    :key="index"
                  >
                    <td>{{ section.course_title }}</td>
                    <td>
                      {{ section.curriculum_abbr }} {{ section.course_number }}
                    </td>
                    <td>{{ section.credits }}</td>
                    <td>{{ section.grade }}</td>
                  </tr>
                </tbody>
              </table>
            </axdd-tab-panel>
          </template>
          <template v-else> Schedule information not available </template>
        </template>
      </axdd-tabs>
    </template>
  </axdd-card>
</template>

<script>
import { Card, CardHeading, Tabs, TabItem, TabPanel } from "axdd-components";

export default {
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-tabs": Tabs,
    "axdd-tab-item": TabItem,
    "axdd-tab-panel": TabPanel,
  },
  props: {
    schedules: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {};
  },
};
</script>
