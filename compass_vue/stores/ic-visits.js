import { defineStore } from "pinia";
import {
  getActiveICVisits,
  studentVisitSearch
} from "@/utils/data";

export const useICVisitsStore = defineStore("icVisits", {
  state: () => {
    return {

      _activeICVisits: {},
      _studentVisits: {}

    };
  },
  getters: {
    activeICVisits(state) {
      if (
        !Object.prototype.hasOwnProperty.call(this._activeICVisits, "request")
      ) {
        this._activeICVisits.request = getActiveICVisits().then(
          (response) => {
            this._activeICVisits.data = response;
          }
        );
      }
      return this._activeICVisits.data;
    },
  },
  actions: {
    async fetchStudentVisit(identifier) {
      if (
        !Object.prototype.hasOwnProperty.call(this._studentVisits, identifier)
      ) {
        this._studentVisits[identifier] = {};
        this._studentVisits[identifier].request = studentVisitSearch(identifier).then(
          (response) => {
            this._studentVisits[identifier].data = response;
          }
        );
      }
      return this._studentVisits[identifier].request;
    },
    getStudentVisitData(identifier) {
      return this._studentVisits[identifier]?.data;
    }
  },
});
