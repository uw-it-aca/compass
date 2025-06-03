import { defineStore } from "pinia";
import { getStudentTranscripts } from "@/utils/data";

export const useStudentStore = defineStore("student", {
  state: () => {
    return {
      getStudentTranscripts,
      transcripts: {},
    };
  },
  getters: {},
  actions: {
    fetchStudentTranscripts(uwregid) {
      if (!Object.prototype.hasOwnProperty.call(this.transcripts, uwregid)) {
        this.transcripts[uwregid] = {
          request: this.getStudentTranscripts(uwregid).then((response) => {
            this.transcripts[uwregid].data = response;
          }),
        };
      }
      return this.transcripts[uwregid].request;
    },
  },
});
