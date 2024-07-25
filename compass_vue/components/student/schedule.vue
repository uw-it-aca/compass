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
                    <template
                      v-for="(section, index) in schedule.sections"
                      :key="index"
                    >
                      <tr
                        :class="[
                          isQuizSection(section.credits) ? 'border-white' : '',
                        ]"
                      >
                        <td class="d-flex ps-3">
                          <!-- Expend and collapse RAD data.
                         Auto expand all classes with a warning icon -->
                          <i class="bi bi-chevron-up me-3 pt-2 h5"></i>
                          <i class="bi bi-chevron-down me-3 pt-2 h5"></i>

                          <div>
                            {{ section.curriculum_abbr }}
                            {{ section.course_number }}
                            {{ section.section_id }}
                            <div class="fs-8 text-secondary">
                              {{ section.course_title }}
                            </div>
                          </div>
                          <!-- If student is predicted to fail the course. -->
                          <i
                            class="bi bi-exclamation-triangle-fill ms-5"
                            style="color: #c12c2c"
                          ></i>
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
                      <!-- MARK: only show course analytics for top-level (i.e. NOT quiz sections)-->
                      <tr v-show="isQuizSection(section.credits)">
                        <td colspan="5" class="p-3 pt-0">
                          <CourseAnalytics></CourseAnalytics>
                        </td>
                      </tr>
                    </template>
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
import { translateMilitaryTime } from "@/utils/translations";
import { getStudentSchedules } from "@/utils/data";
import CourseAnalytics from "@/components/student/analytics/canvas-course.vue";

export default {
  components: {
    CourseAnalytics,
  },
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  setup() {
    return {
      translateMilitaryTime,
      getStudentSchedules,
    };
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
    isQuizSection: function (credits) {
      if (credits.includes("None")) {
        return false;
      } else if (credits.includes("0.0")) {
        return false;
      } else {
        return true;
      }
    },
  },
};
</script>
