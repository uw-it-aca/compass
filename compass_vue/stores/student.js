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
  },
});
