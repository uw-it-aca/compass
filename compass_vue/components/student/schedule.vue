<template>
  <axdd-card>
    <template #heading-tabs v-if="Object.keys(schedules).length">
      <axdd-card-heading :level="2">Schedule</axdd-card-heading>
      <axdd-card-tabs>
        <axdd-tabs-list :tabs-id="'schedule'" :variant="'tabs'" class="small">
          <template #items>
            <axdd-tabs-item
              v-for="(schedule, index) in schedules"
              :key="index"
              :tabs-id="'schedule'"
              :panel-id="'panel' + index"
              :active-tab="index == 0"
              :variant="'tabs'"
              >{{ schedule.term.quarter }}
              {{ schedule.term.year }}</axdd-tabs-item
            >
          </template>
        </axdd-tabs-list>
      </axdd-card-tabs>
    </template>
    <template v-else #heading>
      <axdd-card-heading :level="2">Schedule</axdd-card-heading>
    </template>
    <template #body>
      <axdd-tabs-display :tabs-id="'schedule'">
        <template #panels>
          <template v-if="Object.keys(schedules).length">
            <axdd-tabs-panel
              v-for="(schedule, scheduleIndex) in schedules"
              :key="scheduleIndex"
              :panel-id="'panel' + scheduleIndex"
              :active-panel="scheduleIndex == 0"
            >
              <div class="table-responsive border rounded-3">
                <table class="table m-0">
                  <thead class="small bg-light text-secondary">
                    <tr>
                      <th class="ps-3">Course</th>
                      <th>Title</th>
                      <th>Credits</th>
                    </tr>
                  </thead>
                  <tbody class="mb-3">
                    <tr
                      v-for="(section, index) in schedule.sections"
                      :key="index"
                    >
                      <td class="ps-3">
                        {{ section.curriculum_abbr }}
                        {{ section.course_number }}
                      </td>
                      <td>{{ section.course_title }}</td>
                      <td>{{ section.credits }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </axdd-tabs-panel>
          </template>
          <template v-else>
            <p>No schedules found</p>
          </template>
        </template>
      </axdd-tabs-display>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "../../mixins/data_mixin.js";
import {
  Card,
  CardHeading,
  CardTabs,
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";

export default {
  mixins: [dataMixin],
  components: {
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-tabs": CardTabs,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      schedules: {},
    };
  },
  created() {
    this.loadStudentSchedules();
  },
  methods: {
    loadStudentSchedules: function () {
      this.getStudentSchedules(this.person.uwregid).then((response) => {
        if (response.data) {
          this.schedules = response.data;
        }
      });
    },
  },
};
</script>
