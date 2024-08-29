






import { defineStore } from "pinia";
import { getStudentCourseAnalytics } from "@/utils/data";

export const useAnalyticsStore = defineStore({
  id: "analytics",
  state: () => {
    return {
      getStudentCourseAnalytics,
      courseAnalyticsData: {},
    };
  },
  getters: {},
  actions: {
    fetchStudentCourseAnalytics(uwnetid, year, quarter, course_id) {
      const dataPath = this.courseAnalyticsData[uwnetid] = this.courseAnalyticsData[uwnetid] || {};
      const yearPath = dataPath[year] = dataPath[year] || {};
      const quarterPath = yearPath[quarter] = yearPath[quarter] || {};

      if (!quarterPath[course_id]) {
        quarterPath[course_id] = {
          request: this.getStudentCourseAnalytics(uwnetid, year, quarter, course_id).then((response) => {
            quarterPath[course_id].data = response.data;
          }),
        };
      }
      return quarterPath[course_id].request;
    }
  },
});
