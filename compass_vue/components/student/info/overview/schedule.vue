<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <axdd-card>
    <template #heading-action v-if="Object.keys(schedules).length">
      <axdd-card-heading :level="2">Schedule</axdd-card-heading>
      <axdd-card-tabs>
        <axdd-tabs-list :tabs-id="'schedule'" :variant="'pills'" class="small">
          <template #items>
            <axdd-tabs-item
              v-for="(schedule, index) in schedules"
              :key="index"
              :tabs-id="'schedule'"
              :panel-id="'panel' + index"
              :active-tab="index == 0"
              :variant="'pills'"
            >
              {{ schedule.term.quarter }} {{ schedule.term.year }}
              <span
                v-if="schedule.sections.length > 0"
                class="badge text-bg-purple ms-2 rounded-pill"
                style="min-width: 25px"
                @click.stop
                >{{ getCreditTotal(schedule.sections) }}</span
              >
            </axdd-tabs-item>
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
              <div class="table-responsive m-n3">
                <table class="table m-0">
                  <col style="width: 40%" />
                  <col style="width: 15%" />
                  <col style="width: 13%" />
                  <col style="width: 22%" />
                  <col style="width: 10%" />
                  <thead class="table-light text-muted small">
                    <tr>
                      <th class="ps-3">Course</th>
                      <th>SLN</th>
                      <th>Day</th>
                      <th>Time</th>
                      <th>Credits</th>
                    </tr>
                  </thead>
                  <tbody class="mb-3" v-if="schedule.sections.length > 0">
                    <tr
                      v-for="(section, index) in schedule.sections"
                      :key="index"
                    >
                      <td class="ps-3">
                        {{ section.curriculum_abbr }}
                        {{ section.course_number }}
                        {{ section.section_id }}
                        <div class="fs-8 text-secondary">
                          {{ section.course_title }}
                        </div>
                      </td>
                      <td>{{ section.sln }}</td>
                      <td>
                        <div
                          v-for="(meeting, index) in section.meetings"
                          :key="index"
                        >
                          <span
                            v-for="(value, day) in meeting.meeting_days"
                            :key="day"
                          >
                            <span v-if="value">
                              <span v-if="day == 'monday'">M </span>
                              <span v-if="day == 'tuesday'">T </span>
                              <span v-if="day == 'wednesday'">W </span>
                              <span v-if="day == 'thursday'">Th </span>
                              <span v-if="day == 'friday'">F </span>
                            </span>
                          </span>
                        </div>
                      </td>
                      <td>
                        <div
                          v-for="(meeting, index) in section.meetings"
                          :key="index"
                        >
                          <span v-if="!meeting.no_meeting">
                            {{ translateMilitaryTime(meeting.start_time) }} -
                            {{ translateMilitaryTime(meeting.end_time) }}
                          </span>
                        </div>
                      </td>
                      <td>{{ section.credits }}</td>
                    </tr>
                  </tbody>
                  <tbody v-else class="mb-3">
                    <tr>
                      <td colspan="5" class="ps-3 text-secondary">
                        No registrations found
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </axdd-tabs-panel>
          </template>
          <template v-else>
            <div class="text-secondary">No schedules found</div>
          </template>
        </template>
      </axdd-tabs-display>
    </template>
  </axdd-card>
</template>

<script>
import dataMixin from "@/mixins/data_mixin.js";
import { translateMilitaryTime } from "@/utils/translations";

export default {
  mixins: [dataMixin],
  components: {},
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return { translateMilitaryTime };
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
    getCreditTotal: function (sections) {
      // get all section credits and sum the total
      let creditTotal = 0;
      for (let i = 0; i < sections.length; i++) {
        // parseInt to exclude non-interger credits (i.e. None, NC, etc.)
        if (parseInt(sections[i].credits)) {
          creditTotal += parseInt(sections[i].credits);
        }
      }
      return creditTotal;
    },
  },
};
</script>
