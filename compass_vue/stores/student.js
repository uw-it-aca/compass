import { defineStore } from "pinia";
import { getStudentTranscripts } from "@/utils/data";

export const useStudentStore = defineStore({
  id: "student",
  state: () => {
    return {
      getStudentTranscripts,
      studentData: {},
    };
  },
  getters: {},
  actions: {
    fetchStudentTranscripts(uwregid) {
      if (!Object.prototype.hasOwnProperty.call(this.studentData, uwregid)) {
        this.studentData[uwregid] = {
          request: this.getStudentTranscripts(uwregid).then((response) => {
            this.studentData[uwregid].data = response.data;
          }),
        };
      }
      return this.studentData[uwregid].request;
    },
  },
});
