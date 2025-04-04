import { defineStore } from "pinia";
import {
  getStudentCourseAnalytics,
  getStudentSigninAnalytics,
} from "@/utils/data";

export const useAnalyticsStore = defineStore({
  id: "analytics",
  state: () => {
    return {
      getStudentCourseAnalytics,
      getStudentSigninAnalytics,
      courseAnalyticsData: {},
      signinAnalyticsData: {},
    };
  },
  getters: {},
  actions: {
    fetchStudentSigninAnalytics(uwnetid) {
      if (!this.signinAnalyticsData[uwnetid]) {
        this.signinAnalyticsData[uwnetid] = {
          request: this.getStudentSigninAnalytics(uwnetid).then((response) => {
            this.signinAnalyticsData[uwnetid].data = response;
          }),
        };
      }
      return this.signinAnalyticsData[uwnetid].request;
    },
    fetchStudentCourseAnalytics(uwnetid, year, quarter, course_id) {
      const dataPath = (this.courseAnalyticsData[uwnetid] =
        this.courseAnalyticsData[uwnetid] || {});
      const yearPath = (dataPath[year] = dataPath[year] || {});
      const quarterPath = (yearPath[quarter] = yearPath[quarter] || {});

      if (!quarterPath[course_id]) {
        quarterPath[course_id] = {
          request: this.getStudentCourseAnalytics(
            uwnetid,
            year,
            quarter,
            course_id
          ).then((response) => {
            quarterPath[course_id].data = response;
          }),
        };
      }
      return quarterPath[course_id].request;
    },
  },
});
