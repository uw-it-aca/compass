import { defineStore } from "pinia";
import { getStudentTranscripts } from "@/utils/data";

const SCHOLARSHIP_TYPES = {
  "1": "Dean's List",
  "3": "Warning",
  "4": "Alert",
  "5": "Drop",
  "6": "Reinstate",
  "7": "High Warning",
  "8": "Registrar Reinstate",
  "9": "Pending",
};

export const useStudentStore = defineStore("student", {
  state: () => {
    return {
      getStudentTranscripts,
      transcripts: {},
      scholarshipTypes: SCHOLARSHIP_TYPES,
    };
  },
  getters: {},
  actions: {
    academicStanding(scholarship_code) {
      return (scholarship_code)
        ? this.scholarshipTypes[scholarship_code] : null;
    },
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
