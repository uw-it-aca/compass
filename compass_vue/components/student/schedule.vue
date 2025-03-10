<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <BCard
    class="shadow-sm rounded-3"
    header-class="p-3 d-flex align-items-center justify-content-between"
    body-class="p-0"
    header-bg-variant="transparent"
  >
    <template #header>
      <div class="fs-6 fw-bold">Schedule</div>
      <div v-if="Object.keys(schedules).length">
        <STabsList :tabs-id="'schedule'" :variant="'pills'" class="small">
          <STabsItem
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
              class="badge text-body bg-primary-subtle ms-2 rounded-pill"
              style="min-width: 25px; margin-bottom: 2px;"
              @click.stop
              >{{ getCreditTotal(schedule.sections) }}</span
            >
          </STabsItem>
        </STabsList>
      </div>
    </template>

    <!-- schedule content here-->
    <STabsDisplay :tabs-id="'schedule'">
      <template v-if="Object.keys(schedules).length">
        <STabsPanel
          v-for="(schedule, scheduleIndex) in schedules"
          :key="scheduleIndex"
          :panel-id="'panel' + scheduleIndex"
          :active-panel="scheduleIndex == 0"
        >
          <div class="table-responsive m-0">
            <table class="table m-0">
              <col style="width: 40%" />
              <col style="width: 15%" />
              <col style="width: 13%" />
              <col style="width: 22%" />
              <col style="width: 10%" />
              <thead class="text-muted small">
                <tr>
                  <th class="ps-3 bg-body-tertiary">Course</th>
                  <th class="bg-body-tertiary">SLN</th>
                  <th class="bg-body-tertiary">Day</th>
                  <th class="bg-body-tertiary">Time</th>
                  <th class="bg-body-tertiary">Credits</th>
                </tr>
              </thead>
              <tbody v-if="schedule.sections.length > 0">
                <template
                  v-for="(section, sectionIndex) in schedule.sections"
                  :key="sectionIndex"
                >
                  <tr>
                    <td class="ps-3" :class="isLecture(section.credits) ? 'border-0' : ''">
                      <!-- MARK: only show course analytics for top-level (i.e. NOT quiz sections) v-show="isQuizSection(section.credits)"-->
                      <!-- Expend and collapse RAD data. Auto expand all classes with a warning icon -->
                      <div class="d-flex">
                        <div v-show="isLecture(section.credits)">
                          <button
                            class="btn btn-link chevron text-body"
                            type="button"
                            data-bs-toggle="collapse"
                            :data-bs-target="'#collapseDiv_' + scheduleIndex + '_' + sectionIndex"
                            aria-expanded="false"
                            :aria-controls="'collapseDiv_' + scheduleIndex + '_' + sectionIndex"
                          >
                            <i
                              class="bi bi-chevron-down"
                              aria-hidden="true"
                            ></i>
                          </button>
                        </div>
                        <div>
                          {{ section.curriculum_abbr }}
                          {{ section.course_number }}
                          {{ section.section_id }}
                          <div class="fs-8 text-secondary">
                            {{ section.course_title }}
                          </div>
                        </div>

                        <i
                          v-if="section.alert_status"
                          class="bi bi-exclamation-triangle-fill ms-5"
                          style="color: #c12c2c"
                        ></i>
                      </div>
                    </td>
                    <td :class="isLecture(section.credits) ? 'border-0' : ''">
                      {{ section.sln }}
                    </td>
                    <td :class="isLecture(section.credits) ? 'border-0' : ''">
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
                    <td :class="isLecture(section.credits) ? 'border-0' : ''">
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
                    <td :class="isLecture(section.credits) ? 'border-0' : ''">
                      {{ section.credits }}
                    </td>
                  </tr>
                  <!-- MARK: show course analytics only for lecture courses -->
                  <tr v-if="isLecture(section.credits)">
                    <td colspan="5" class="p-0">
                      <div
                        class="collapse"
                        :id="'collapseDiv_' + scheduleIndex + '_' + sectionIndex"
                        v-on="{'shown.bs.collapse': expandCourseAnalytics}"
                      >
                        <CourseAnalytics
                          v-if="getAnalyticsVisibility('collapseDiv_' + scheduleIndex + '_' + sectionIndex)"
                          :uwnetid="person.uwnetid"
                          :year="schedule.year"
                          :quarter="schedule.quarter"
                          :course_id="`${section.curriculum_abbr} ${section.course_number} ${section.section_id}`"
                        ></CourseAnalytics>
                      </div>
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
        </STabsPanel>
      </template>
      <div v-else class="p-3">No schedules found.</div>
    </STabsDisplay>
  </BCard>
</template>

<script>
import { translateMilitaryTime } from "@/utils/translations";
import { getStudentSchedules } from "@/utils/data";
import CourseAnalytics from "@/components/student/analytics/canvas-course.vue";
import { BCard } from "bootstrap-vue-next";
import { STabsDisplay, STabsPanel, STabsList, STabsItem } from "solstice-vue";

export default {
  components: {
    CourseAnalytics,
    BCard,
    STabsDisplay,
    STabsPanel,
    STabsList,
    STabsItem,
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
      analyticsDisplay: {},
    };
  },
  created() {
    this.loadStudentSchedules();
  },
  methods: {
    getAnalyticsVisibility: function (target) {
      return this.analyticsDisplay[target] == true;
    },
    expandCourseAnalytics(event) {
      this.analyticsDisplay[event.currentTarget.id] = true;
    },
    loadStudentSchedules: function () {
      this.getStudentSchedules(this.person.uwregid).then((response) => {
        if (response) {
          this.schedules = response;
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
    isLecture: function (credits) {
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

<style lang="scss" scoped>
.chevron .bi-chevron-down {
  display: inline-block;
  transition: transform 0.25s ease;
  transform-origin: 0.5em 50%;
  font-weight: bolder;
}

.chevron[aria-expanded="true"] .bi-chevron-down {
  transform: rotate(-180deg);
}

.bi-chevron-down::after {
  font-weight: bolder !important;
}
</style>
