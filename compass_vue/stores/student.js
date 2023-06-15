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
      if (!Object.prototype.hasOwnProperty.call(this.studentData, uwregid)) {
        this.studentData[uwregid] = {
          request: dataMixin.methods
            .getStudentTranscripts(uwregid)
            .then((response) => {
              this.studentData[uwregid].data = response.data;
            }),
        };
      }
      return this.studentData[uwregid].request;
    },
    getStudentSchedules(uwregid) {
      // Returns a student schedule for the current and next two terms
      let schedules = [];
      this.studentData[uwregid].data.forEach((transcript) => {
        try {
          if (transcript.class_schedule.display_schedule === true){
            schedules.push(transcript.class_schedule);
          }
        } catch (e) {
          //  no transcript
        }
      });
      return schedules;
    },
  },
});
