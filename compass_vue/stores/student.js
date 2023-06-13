import {defineStore} from "pinia";
import dataMixin from "../mixins/data_mixin.js";

export const useStudentStore = defineStore({
  id: "student",
  state: () => {
    return {
      studentData: {},
    };
  },
  getters: {},
  actions: {
    fetchStudentTranscripts(uwregid) {
      if (Object.prototype.hasOwnProperty.call(this.studentData, uwregid)) {
        return this.studentData[uwregid].request;
      } else {
        this.studentData[uwregid] = {
          request: dataMixin.methods
            .getStudentTranscripts(uwregid).then((response) => {
              this.studentData[uwregid].data = response.data;
            }),
        };
        return this.studentData[uwregid].request;
      }
    },
    getStudentSchedules(uwregid) {
      let schedules = [];
      this.studentData[uwregid].data.forEach((transcript) => {
        schedules.push(transcript.class_schedule);
      });
      return schedules;
    },
  },
});
